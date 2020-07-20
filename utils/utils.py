import z3
import json
import torch
from Doping.pytorchtreelstm.treelstm import calculate_evaluation_orders
# from Doping.PySpacerSolver.utils import *
import os
import numpy as np

def get_exp_name(prefix, exp_folder, vis, use_c, use_const_emb, use_dot_product, max_size, shuffle, negative_sampling_rate, threshold):
    '''
    construct a meaningful exp_name for the Tensorboard
    '''
    exp_name = []
    #exp_folder is in the form
    #"PySpacerSolver/MEDIA/backward_encoded_split_on_relu.smt2_250220_13_04_22/ind_gen_files/"
    exp_name.append(exp_folder.split("/")[-3])
    exp_name.append(prefix+"_")
    if vis:
        exp_name.append("V")
    if use_c:
        exp_name.append("C")
    if use_const_emb:
        exp_name.append("E")
    if use_dot_product:
        exp_name.append("D")
    exp_name.append("M")
    exp_name.append(str(max_size))
    exp_name.append("Nr")
    exp_name.append(str(negative_sampling_rate))
    exp_name.append("Th")
    exp_name.append(str(threshold))
    if shuffle:
        exp_name.append("S")

    return "_".join(exp_name)

def json_to_markdown(data):
    result = ""
    for key in data:
        result += "### %s\n"%key
        result += "```\n"
        result += "%s"%(str(data[key]).replace("\n", "\n\n"))
        result += "\n```"
        result += "\n"

    return result


def display_example(filename, true_label, pred_label, value):
    label_texts = ["SAME COLOR", "DIFFERENT COLOR"]
    with open(filename, "r") as dp:
        datapoint = json.load(dp)
    label_in_file = datapoint["label"]
    assert(label_in_file == true_label)

    C_tree = datapoint["C_tree"]
    L_a_tree = datapoint["L_a_tree"]
    L_b_tree = datapoint["L_b_tree"]

    C_tree_expr = C_tree["children"][0]["expr"]
    L_a_tree_expr = L_a_tree["children"][0]["expr"]
    L_b_tree_expr = L_b_tree["children"][0]["expr"]


    result = {}
    result["filename"] = "..." + filename[-20:]
    result["C_tree_expr"] = C_tree_expr
    result["L_a_tree_expr"] = L_a_tree_expr
    result["L_b_tree_expr"] = L_b_tree_expr
    result["value"] = value
    result["pred_label"] = label_texts[pred_label]
    result["true_label"] = label_texts[label_in_file]

    #Tensorboard use markdown to render text
    return json_to_markdown(result)

def calculate_P(X, L, L_freq):
    idx2freq = {}
    for k in L:
        idx = L[k]
        freq = L_freq[k]

        idx2freq[idx] = freq
    print(len(X), len(L), len(L_freq))
    assert(len(X)==len(L)==len(L_freq))
    P_matrix = np.zeros((len(X), len(X)))
    for i in range(len(X)):
        for j in range(len(X)):
            #P_matrix[i][j] = P(lit_i|lit_j)
            P_matrix[i][j] = X[i][j]/idx2freq[j]
            assert(P_matrix[i][j]<=1 )

    return P_matrix
