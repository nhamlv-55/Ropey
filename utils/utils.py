import z3
import json
import torch
from Doping.pytorchtreelstm.treelstm import calculate_evaluation_orders
# from Doping.PySpacerSolver.utils import *
import os

def get_exp_name(exp_folder, vis, use_c, use_const_emb, max_size, shuffle):
    exp_name = []
    #exp_folder is in the form
    #"PySpacerSolver/MEDIA/backward_encoded_split_on_relu.smt2_250220_13_04_22/ind_gen_files/"
    exp_name.append(exp_folder.split("/")[-3])
    if vis:
        exp_name.append("V")
    if use_c:
        exp_name.append("C")
    if use_const_emb:
        exp_name.append("E")
    exp_name.append("M")
    exp_name.append(str(max_size))
    if shuffle:
        exp_name.append("S")

    return "_".join(exp_name)
    
