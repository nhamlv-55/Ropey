# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import argparse
import grpc

import indgen_conn_pb2
import indgen_conn_pb2_grpc
import glob
import os
import Doping.PySpacerSolver.spacer_solver as SS
import subprocess

import Doping.PySpacerSolver.utils as DPu
from Doping.PySpacerSolver.ExprDb import ExprDb
from Doping.utils.utils import get_seed_file
from RNN_eval import setup_model
from six.moves import cStringIO

import torch
import torch.nn as nn
from Doping.pytorchtreelstm.treelstm import batch_tree_input
import json

#(lit_56, lit_55)
TEST1 = ["not( = invariant_33_n 3)","not(= invariant_33_n 2)"]

class Lemma_Dp:
    def __init__(self, exp_folder, new_folder, prefix = ""):
        self.lemma = ""
        self.level = -1
        self.smtfile = None
        self.new_folder = new_folder
        self.exp_folder = exp_folder
        self.prefix = prefix

    def to_smt2(self):
        if not os.path.exists(os.path.join(self.exp_folder, self.new_folder)):
            os.makedirs(os.path.join(self.exp_folder, self.new_folder))

        if self.smtfile is None: return
        with open(os.path.join(self.exp_folder, self.smtfile), "r") as f:
            old_file_lines = f.readlines()
            params = old_file_lines[-1]
            if "dump_threshold 5.00 " in params:
                return
        new_filename = self.smtfile + ".with_lemma"+self.prefix+".smt2"
        with open(os.path.join(self.exp_folder, self.new_folder, new_filename), "w") as f:
            f.writelines(old_file_lines)
            f.write("\n")
            f.write("(act-lvl %s)\n"%(self.level))
            f.write("(ind-gen %s)\n"%(self.lemma))

class Greeter(indgen_conn_pb2_grpc.GreeterServicer):
    def __init__(self, server_config):
        print("init server")
        self.exp_folder = server_config["exp_folder"]
        self.new_folder = server_config["new_folder"]
        self.model = server_config["model"] 
        self.dataset = server_config["dataset"]
        self.seed_path = server_config["seed_path"]
        self.fallback_mode = server_config["fallback_mode"]
        self.random_mode = server_config["random_mode"]
        if not self.fallback_mode:
            self.seed_file = get_seed_file(self.seed_path)
            self.edb = ExprDb(self.seed_file)
        else:
            self.seed_file = None
            self.edb = None
        self.last_request = None
        self.m = nn.Softmax(dim = 1)

        self.cached_lemma = None
        self.cached_lits = None
        self.cached_lit_jsons = None

        self.cached_P_mat = None
        self.cached_N_mat = None
        # self.run_test(TEST1)

    def SayHello(self, request, context):
        return indgen_conn_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SendLemma(self, request, context):
        """
        NOT USED
        """
        if len(self.lemmas_q) < self.max_q:
            self.lemmas_q.append(self.request_to_dp(request))
            logging.info("Before:", request.lemma_before)
            logging.info("After:", request.lemma_after)
            return indgen_conn_pb2.Ack(ack_message=True)
        else:
            if not self.is_training:
                self.train()
                self.is_training = True
            return indgen_conn_pb2.Ack(ack_message=False)

    def fallback_answer(self, to_be_checked_lits, kept_lits, mask, dirty = False):
        print("fallback ans:")
        if len(to_be_checked_lits)>0:
            checking_lits = [to_be_checked_lits[0]]
            to_be_checked_lits = to_be_checked_lits[1:]
        else:
            checking_lits = []
        for i in kept_lits:
            mask[i] = 1
        for i in to_be_checked_lits:
            mask[i] = 1
        for i in checking_lits:
            mask[i] = 0
        print("mask", mask)
        print("new_tobechecked_lits", to_be_checked_lits)
        print("new kept lits", kept_lits)
        print("checking_lits", checking_lits)
        return indgen_conn_pb2.FullAnswer(dirty = dirty,
                                            mask = mask,
                                            new_to_be_checked_lits = to_be_checked_lits,
                                            new_kept_lits = kept_lits,
                                            checking_lits = checking_lits)
    def random_answer(self, to_be_checked_lits, kept_lits, mask, dirty = False):
        if len(to_be_checked_lits)>0:
            checking_lits = [to_be_checked_lits[0]]
            to_be_checked_lits = to_be_checked_lits[1:]
        else:
            checking_lits = []
        for i in kept_lits:
            mask[i] = 1
        for i in to_be_checked_lits:
            mask[i] = 1
        for i in checking_lits:
            mask[i] = 0
        return indgen_conn_pb2.FullAnswer(dirty = dirty,
                                            mask = mask,
                                            new_to_be_checked_lits = to_be_checked_lits,
                                            new_kept_lits = kept_lits,
                                            checking_lits = checking_lits)


    def QueryMask(self, request, context):
        """
        Input:
        - lemma (a list of literals)
        - kept_lits (a list of indices of literals that are kept)
        - to_be_checked_lits (a list of indices of literals that we haven't seen yet)
        - checking_lit is a dummy number. We are not using it now
        Output:
        - A dirty bit telling the solver whether to use the answer or not
        - A binary mask of what literal should be stay(1) and what literal should be tried to drop/set to true(0)
            The mask should have the same size as the lemma
        - A new kept_lits list
        - A new to_be_checked_lits list
        """
        lemma = request.lemma
        first_query = (request.lemma != "")
        if lemma!="":#receive a new lemma, invalidate cache
            self.cached_lemma = lemma
            self.cached_lits = None
            self.cached_lit_jsons = None
            self.cached_N_mat = None
            self.cached_P_mat = None
        kept_lits = request.kept_lits
        to_be_checked_lits = request.to_be_checked_lits
        lemma_size = request.lemma_size
        # default mask
        mask = [0]*lemma_size
        # is the mask updated?
        mask_updated = False
        # are kept_lits and to_be_checked_lits updated?
        lists_updated = False
        print("Last ans success:", request.last_ans_success)
        print("Receive lemma:", lemma)
        print("kept_lits", kept_lits)
        print("to_be_checked_lits", to_be_checked_lits)


        """
        FALLBACK MODE
        """
        if self.fallback_mode or self.seed_file is None:
            print("fall back mode is on")
            return self.fallback_answer(to_be_checked_lits, kept_lits, mask)
        if request == self.last_request:
            return self.fallback_answer(to_be_checked_lits, kept_lits, mask)
        if lemma == "" or lemma_size ==1:
            print("not the first query or lemma_size = 1")
            return self.fallback_answer(to_be_checked_lits, kept_lits, mask)
        #update cache
        self.last_request = request
        print(self.cached_lemma)
        output = self.model(self.parse_and_batch_input(self.cached_lemma))
        m = nn.Softmax(dim = 1)

        values, pred = torch.max(m(output), 1)

        print(values, pred)
        mask = pred.cpu().tolist()
        print(mask)
        # print(output)
        # exit(0)
        return indgen_conn_pb2.FullAnswer(dirty = True,
                                        mask = mask,
                                        new_kept_lits = kept_lits,
                                        new_to_be_checked_lits = to_be_checked_lits,
                                        checking_lits = [-1, -1])#any checking lits longer than 1 will trigger spacer grpc to go with fallback mode

    def dump_model_res(self, kept_lits, to_be_checked_lits, output):
        output = output.tolist()
        counter = 0
        for tobechecked_idx in to_be_checked_lits:
            for kept_idx in kept_lits:
                print("f(l_{},l_{}) = {}".format(tobechecked_idx, kept_idx, output[counter]))
                counter+=1



    def parse_and_batch_input(self, lemma):
        lit_jsons, lits = self.parse_lemma(lemma)
        print("no of lits:", len(lit_jsons))
        return batch_tree_input([ DPu.convert_tree_to_tensors(lit["tree"]) for lit in lit_jsons])



    def run_test(self, cube):
        print("Running test on cube", cube)
        lemma = "(and ({}) ({}))".format(cube[0], cube[1])
        kept_lits = [0]
        checking_lit = 1
        to_be_checked_lits = []

        self.predict_core(lemma, kept_lits, checking_lit, to_be_checked_lits)

    def parse_lemma(self, lemma):
        """
        Given a lemma in a str format, parse it into:
        - a list of literals in SMT2 format, and
        - a list of literals in JSON format
        NOTE:This is very ugly for now
        """
        if self.cached_lit_jsons is not None:
            return self.cached_lit_jsons, self.cached_lits
        else:
            #parse the lemma to PySMT representation
            lemma_cmd = "\n(ind-gen {})\n".format(self.cached_lemma)
            # print(lemma_cmd)
            all_cmds = self.edb.parser.get_script(cStringIO(lemma_cmd)).commands
            assert(len(all_cmds)==1)
            assert(all_cmds[0].name == "ind-gen")
            cmd = all_cmds[0]

            print(cmd)
            lits = [self.edb.converter.convert(v) for v in cmd.args.args()]
            # Use the dataset object to parse it to JSON.
            lit_jsons = self.dataset.parse_cube_to_lit_jsons(lits)
            assert(len(lit_jsons)==len(lits))

            #update cache
            self.cached_lits = lits
            self.cached_lit_jsons = lit_jsons

        return lit_jsons, lits

def serve(server_config, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    indgen_conn_pb2_grpc.add_GreeterServicer_to_server(Greeter(server_config), server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--input', help='path to the smt2 files generated by running z3')
    parser.add_argument('-S', '--seed-path', help='path to the folder containing the seed pool_solver indgen smt2 query file')
    parser.add_argument("-L", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    parser.add_argument('-M', '--model-path', help='path to the .pt file of the RNN model')
    parser.add_argument('-p', '--port', default='50051', help='port to serve the grpc server')
    parser.add_argument('-F', '--fallback-mode', action='store_true', help='whether to run in fallback mode')
    parser.add_argument('-R', '--random-mode', action='store_true', help='whether to run in fallback mode')
    args = parser.parse_args()

    fallback_mode = args.fallback_mode
    if fallback_mode:
        port = args.port
        server_config={
            "exp_folder": None,
            "new_folder": None,
            "model": None, #negative model
            "dataset": None,
            "seed_path": None,
            "fallback_mode": args.fallback_mode,
            "random_mode": False
        }
    else:
        exp_folder = args.input
        new_folder = "ind_gen_files"
        seed_path = args.seed_path
        #need the dataset object to parse the received lemma
        dataset = DPu.Dataset(folder = os.path.dirname(args.input))
        #use the vocab of the dataset
        dataset.vocab.load(os.path.join(args.input,"vocab.json"))
        dataset.vocab.dump()
        port = args.port
        model = setup_model(args.model_path)
        server_config={
            "exp_folder": exp_folder,
            "new_folder": new_folder,
            "model": model, #positive model
            "dataset": dataset,
            "seed_path": seed_path,
            "fallback_mode": args.fallback_mode,
            "random_mode": args.random_mode
        }

    print(server_config)
    serve(server_config, port)
