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
from X_eval import setup_model
from six.moves import cStringIO

import torch
import torch.nn as nn
from Doping.pytorchtreelstm.treelstm import batch_tree_input
import json

#(lit_56, lit_55)
TEST1 = ["not( = invariant_33_n 3)","not(= invariant_33_n 2)"]

#only trigger N_MODEL if kept_lits has more than N_MODEL_LIM
N_MODEL_LIM = 1
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
        self.p_model = server_config["p_model"] #positive model
        self.n_model = server_config["n_model"] #negative model
        self.dataset = server_config["dataset"]
        self.seed_path = server_config["seed_path"]
        self.fallback_mode = server_config["fallback_mode"]
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

        # print("N model:", self.n_model)
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

    # def QueryModel(self, request, context):
    #     """
    #     Input:
    #     - lemma (a list of literals)
    #     - kept_lits (a list of indices of literals that are kept)
    #     - checking_lit (index of the literal we want to check)
    #     - to_be_checked_lits (a list of indices of literals that we haven't seen yet)

    #     Output:
    #     - A list of indices of literal that we should try to drop
    #     NOTE: for now, we only return either:
    #     - []: empty list ~ should keep the checking_lit literal
    #     - [checking_lit]:  should try to drop the checking_lit 
    #     """

    #     lemma = request.lemma
    #     kept_lits = request.kept_lits
    #     to_be_checked_lits = request.to_be_checked_lits
    #     lemma_size = request.lemma_size
    #     print("Receive lemma:", lemma)

    #     L_a_batch, L_b_batch = self.parse_and_batch_input(lemma, kept_lits, to_be_checked_lits)
        

    #     # in positive_pairs, if a pair value is 1, that means it has very high correlation
    #     output = self.p_model(L_a_batch, L_b_batch)[0]
    #     values, pos_pred = torch.max(self.m(output), 1)
    #     positive_pairs = pos_pred.tolist()

    #     # in negative_pairs, if a pair value is 0, that means if 1 of the pair exists in the lemma, the other should not be there.
    #     output = self.n_model(L_a_batch, L_b_batch)[0]
    #     values, neg_pred = torch.max(self.m(output), 1)
    #     negative_pairs = neg_pred.tolist()

    #     #print for debugging
    #     for i in range(len(positive_pairs)):
    #         if i%len(kept_lits)==0:
    #             print("----------------------")
    #         print(positive_pairs[i], negative_pairs[i])
        
    #     # build answer using positive_pairs and negative_pairs

    #     return indgen_conn_pb2.Answer(answer = answer)

    def fallback_answer(self, to_be_checked_lits, kept_lits, mask):
            checking_lits = [to_be_checked_lits[0]]
            to_be_checked_lits = to_be_checked_lits[1:]
            for i in kept_lits:
                mask[i] = 1
            for i in to_be_checked_lits:
                mask[i] = 1
            for i in checking_lits:
                mask[i] = 0
            return indgen_conn_pb2.FullAnswer(dirty = False,
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
        if lemma!="":#receive a new lemma, invalidate cache
            self.cached_lemma = lemma
            self.cached_lits = None
            self.cached_lit_jsons = None
        kept_lits = request.kept_lits
        to_be_checked_lits = request.to_be_checked_lits
        lemma_size = request.lemma_size
        # default mask
        mask = [0]*lemma_size
        # is the mask updated?
        mask_updated = False
        # are kept_lits and to_be_checked_lits updated?
        lists_updated = False
        if not request.last_ans_success:
            print("Last ans success:", request.last_ans_success)
            print("Receive lemma:", lemma)
            print("kept_lits", kept_lits)
            print("to_be_checked_lits", to_be_checked_lits)

        """
        FALLBACK MODE
        """
        if self.fallback_mode or request == self.last_request or len(kept_lits)==0 or self.seed_file is None:
            return self.fallback_answer(to_be_checked_lits, kept_lits, mask)
        #update cache
        self.last_request = request
        """
        USING ML MODEL MODE
        Q: Should we run P first or N first?

        Q: Should we just create  suggested lists from P and N model
        """
        # suggest a "should be kept list"
        should_be_kept_lits = set()
        if self.p_model is not None and len(kept_lits)*len(to_be_checked_lits)>0:
            # in positive_pairs, if a pair value is 1, that means it has very high correlation
            L_kept_batch, L_2bchecked_batch, lemma_size, lits = self.parse_and_batch_input(lemma, kept_lits, to_be_checked_lits)
            # calculating whether P(lit_2bechecked| lit_kept) > THRESHOLD
            output = self.p_model(L_2bchecked_batch, L_kept_batch)[0]
            values, pos_pred = torch.max(self.m(output), 1)
            positive_pairs = pos_pred.tolist()
            print("p_model calculation")
            self.dump_model_res(kept_lits, to_be_checked_lits, output)

            for i in range(len(to_be_checked_lits)):
                lit_idx = to_be_checked_lits[i]
                #does lit at lit_idx has high correlation with any lit in kept_lits? If yes, move it to kept_lits
                high_cor_with_kept_lits = positive_pairs[i*len(kept_lits):(i+1)*len(kept_lits)]
                print("lit_{} has high cor with kept_lits".format(lit_idx), high_cor_with_kept_lits)
                if 1 in high_cor_with_kept_lits:
                    print("p model found a high cor pair. suggest to keep lit {}".format(lit_idx))
                    should_be_kept_lits.add(lit_idx)

        # update mask using negative_pairs
        # suggest a "should be drop list"
        """
        #collect anti-occurance
        for ori_lit_idx in range(len(ori_cube)):
            L_ori_tree_str = L_ori_trees_str[ori_lit_idx]
            ori_lit_global_idx = self.negative_lit[L_ori_tree_str]
            if L_ori_tree_str not in L_inducted_trees_str:
                #mark all pair into the negative_X matrix
                for inducted_lit_idx in range(len(inducted_cube)):
                    L_inducted_tree_str = L_inducted_trees_str[inducted_lit_idx]
                    inducted_lit_global_idx = self.negative_lit[L_inducted_tree_str]

                    self.negative_X[(ori_lit_global_idx, inducted_lit_global_idx)]+=1
        """
        should_be_drop_lits = set()
        if self.n_model is not None and len(kept_lits)*len(to_be_checked_lits)>0 and len(kept_lits)>N_MODEL_LIM:
            # in negative_pairs, if a pair value is 0, that means if 1 of the pair exists in the lemma, the other should not be there.
            L_kept_batch, L_2bchecked_batch, lemma_size, lits = self.parse_and_batch_input(lemma, kept_lits, to_be_checked_lits)

            output = self.n_model(L_2bchecked_batch, L_kept_batch)[0]
            output = self.m(output)
            print("n_model calculation")
            self.dump_model_res(kept_lits, to_be_checked_lits, output)
            values, neg_pred = torch.max(output, 1)
            negative_pairs = neg_pred.tolist()

            for i in range(len(to_be_checked_lits)):
                lit_idx = to_be_checked_lits[i]
                #does the lit at lit_idx has anti-correlation with any lit in kept_lits? 
                no_cor_with_kept_lits = negative_pairs[i*len(kept_lits):(i+1)*len(kept_lits)]
                print("no cor with kept_lits", no_cor_with_kept_lits)
                if no_cor_with_kept_lits.count(1)>=N_MODEL_LIM:
                    print("lit at id {} has 0 correlation with {} lits in kept_lits. set it to 0".format(lit_idx, no_cor_with_kept_lits.count(1)))
                    should_be_drop_lits.add(lit_idx)

        """
        construct the answer using should_be_kept_lits, should_be_drop_lits
        """


        intersect_set = should_be_drop_lits.intersection(should_be_kept_lits)
        print("intersect between 2 suggestion sets:", intersect_set)
        #there is a conflict, use fallback mode
        if len(intersect_set)>0:
            return self.fallback_answer(to_be_checked_lits, kept_lits, mask)
        else:
            for i in kept_lits:
                mask[i]=1
            for i in to_be_checked_lits:
                mask[i]=1
            for i in should_be_kept_lits:
                mask[i]=1
                kept_lits.append(i)
                to_be_checked_lits.remove(i)
            if len(should_be_drop_lits)==0 and len(to_be_checked_lits)>0:
                return self.fallback_answer(to_be_checked_lits, kept_lits, mask)
            else:
                for i in should_be_drop_lits:
                    mask[i]=0

                checking_lits = should_be_drop_lits
                print("mask", mask)
                print("new_kep_lits", kept_lits)
                print("new_to_be_checked_lits", to_be_checked_lits)
                print("checking_lits", checking_lits)
                print("-------------")
                return indgen_conn_pb2.FullAnswer(dirty = True,
                                                mask = mask,
                                                new_kept_lits = kept_lits,
                                                new_to_be_checked_lits = to_be_checked_lits,
                                                checking_lits = checking_lits)

    def dump_model_res(self, kept_lits, to_be_checked_lits, output):
        output = output.tolist()
        counter = 0
        for tobechecked_idx in to_be_checked_lits:
            for kept_idx in kept_lits:
                print("f(l_{},l_{}) = {}".format(tobechecked_idx, kept_idx, output[counter]))
                counter+=1



    def parse_and_batch_input(self, lemma, kept_lits, to_be_checked_lits):
        lit_jsons, lits = self.parse_lemma(lemma)
        print("no of lits:", len(lit_jsons))

        """
        example:
        with p_model, and
        kept_lits = [0, 1, 4]
        to_be_checked_lits = [5, 6]
        => calculating
        P(l_5|l_0)=0,
        P(l_5|l_1)=0,
        P(l_5|l_4)=0,
        P(l_6|l_0)=0.1,
        P(l_6|l_1)=0.2,
        P(l_6|l_4)=0,
        """
        #batching inputs
        #L_kept_batch = [l_0, l_1, l_4, l_0, l_1, l_4)
        #L_2bchecked_batch = [l_5, l_5, l_5, l_6, l_6, l_6)
        L_kept_trees = []
        L_2bchecked_trees = []
        # print("batching...")
        for tobechecked_idx in to_be_checked_lits:
            for kept_idx in kept_lits:
                # print("kept", kept_idx, "tobechecked", tobechecked_idx)
                L_kept_trees.append(DPu.convert_tree_to_tensors(lit_jsons[kept_idx]["tree"]))
                L_2bchecked_trees.append(DPu.convert_tree_to_tensors(lit_jsons[tobechecked_idx]["tree"]))

        if len(L_kept_trees)>0:
            L_kept_batch = batch_tree_input(L_kept_trees)
            L_2bechecked_batch = batch_tree_input(L_2bchecked_trees)

            return L_kept_batch, L_2bechecked_batch, len(lits), lits
        else:
            return None, None, len(lits), None



    def run_test(self, cube):
        print("Running test on cube", cube)
        lemma = "(and ({}) ({}))".format(cube[0], cube[1])
        kept_lits = [0]
        checking_lit = 1
        to_be_checked_lits = []

        self.predict_core(lemma, kept_lits, checking_lit, to_be_checked_lits)

    def dump_lemmas(self):
        """
        NOT USED
        """
        print("\t\tDumping lemmas")
        self.get_seed_file()
        for idx , (l_before, l_after) in enumerate(self.lemmas_q):
            l_after.smtfile = self.seed_file
            l_after.prefix = str(idx)
            l_after.to_smt2()

    def run_spacer_solver(self):
        """
        NOT USED
        """
        print("Running spacer solver")
        dataset = None
        input = os.path.join(self.exp_folder, self.new_folder)
        limit = 4000
        if os.path.isdir(input):
            dataset = SS.DPu.Dataset(folder = input, html_vis_page = "ind_gen_vis.html")
            SS.skip_ind_gen_folder(input, False, dataset = dataset, limit = limit)

        if dataset is not None:
            dataset.dump_html()

    def run_model_training(self):
        """
        NOT USED
        """
        print("\t\tRunning model training")
        my_env = os.environ.copy()
        my_env["PATH"]="/home/nv3le/workspace/"

        training_cmd = ["/home/nv3le/anaconda3/envs/py3/bin/python", "X_train.py"]
        training_cmd.extend(["-input", os.path.join(self.exp_folder, self.new_folder)])
        training_cmd.extend(["-Nr", "5"])
        print("\t\ttraining cmd: {}".format(" ".join(training_cmd)))
        with open("training.log", "w") as training_log:
            subprocess.Popen(training_cmd, stdout = training_log, env=my_env)

    def train(self):
        """
        NOT USED
        """
        print("\tIn Training")
        self.dump_lemmas()
        self.run_spacer_solver()
        self.run_model_training()

    def request_to_dp(self, request):
        """
        NOT USED
        """
        lemma_before = Lemma_Dp(self.exp_folder, self.new_folder)
        lemma_after = Lemma_Dp(self.exp_folder, self.new_folder)

        for l in request.lemma_before.strip().split("\n"):
            lemma_before.lemma +=l

        for l in request.lemma_after.strip().split("\n"):
            lemma_after.lemma +=l

        return (lemma_before, lemma_after)


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
    parser.add_argument('-P', '--p-model-path', help='path to the .pt file of the positive model')
    parser.add_argument('-N', '--n-model-path', help='path to the .pt file of the negative model')
    parser.add_argument('-p', '--port', default='50051', help='port to serve the grpc server')
    parser.add_argument('-F', '--fallback-mode', action='store_true', help='whether to run in fallback mode')
    args = parser.parse_args()

    fallback_mode = args.fallback_mode
    if fallback_mode:
        port = args.port
        server_config={
            "exp_folder": None,
            "new_folder": None,
            "p_model": None, #positive model
            "n_model": None, #negative model
            "dataset": None,
            "seed_path": None,
            "fallback_mode": args.fallback_mode
        }
    else:
        exp_folder = args.input
        new_folder = "ind_gen_files"
        seed_path = args.seed_path
        #need the dataset object to parse the received lemma
        dataset = DPu.Dataset(folder = os.path.dirname(args.input))
        #use the vocab of the dataset
        dataset.vocab.load(os.path.join(args.input,"vocab.json"))
        port = args.port
        if args.p_model_path is not None:
            p_model = setup_model(args.p_model_path)
        else:
            p_model = None
        if args.n_model_path is not None:
            n_model = setup_model(args.n_model_path)
        else:
            n_model = None
        server_config={
            "exp_folder": exp_folder,
            "new_folder": new_folder,
            "p_model": p_model, #positive model
            "n_model": n_model, #negative model
            "dataset": dataset,
            "seed_path": seed_path,
            "fallback_mode": args.fallback_mode
        }

    print(server_config)
    serve(server_config, port)
