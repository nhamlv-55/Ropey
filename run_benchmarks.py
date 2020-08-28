import os
import subprocess
import argparse
import random
from shutil import copyfile
from os.path import join as pjoin
from constants import FALLBACK_SERVER, FALLBACK_CONFIG, DOPING_CONFIG
import logging
import sys
'''
1. Run the X_grpc server in fallback mode. Keep it running
For each benchmark:
  Create a folder for the benchmark
  Create a folder for the original query
  Generate k variants, each in its own folder
  Run spacer with ind_gen trace to generate file
  Run generate_ind_gen_files.py
  Run spacer_solver
  Run training
  Run X_grpc using the trained model
  For v in variants:
    Run spacer without ind_gen trace against fallback server
    Run spacer without ind_gen trace against X_grpc model server
  Kill X_grpc model server


'''
log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
    format=log_format, datefmt='%m/%d %I:%M:%S %p')
fh = logging.FileHandler('log.txt')
fh.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(fh)


class GrpcServer():
    def __init__(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass

def create_exp_folder(smt2_file):
    exp_folder = pjoin("results", smt2_file.split(".")[0])
    os.makedirs(exp_folder)
    return exp_folder

def generate_variant(filename):
    pass

def start_server(port, fallback = False):
    pass

def run_spacer(folder, config):
    pass

def run_dataset_gen(folder):
    pass

def run_training(folder):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--benchmark_folder', help='path to the folder containing all benchmarks')
    parser.add_argument('-k', '--nvariants', help='number of variants')

    args = parser.parse_args()

    for smt2_file in args.benchmark_folder:
        exp_folder = create_exp_folder(smt2_file)
        copyfile(smt2_file, pjoin(exp_folder, 'original', 'input_file.smt2'))
        for i in range(args.nvariants):
            variant_i = generate_variant(smt2_file)
            variant_folder = pjoin(exp_folder, 'variant_{}'.format(str(i)) )
            os.makedirs(os.path.dirname(variant_folder, exist_ok=True))
            copyfile(variant_i, pjoin(variant_folder, 'input_file.smt2'))

        run_spacer(pjoin(exp_folder, 'original'), FALLBACK_CONFIG)
        run_dataset_gen(pjoin(exp_folder, 'original'))

        run_training(pjoin(exp_folder, 'original'))
        doping_server = start_server(pjoin(exp_folder, 'original', 'model.pt'))

        for i in range(args.nvariants):
            run_spacer(pjoin(exp_folder, 'variant_{}'.format(str(i))),
                       FALLBACK_CONFIG)
            run_spacer(pjoin(exp_folder, 'variant_{}'.format(str(i))),
                       DOPING_CONFIG)
        doping_server.stop()


