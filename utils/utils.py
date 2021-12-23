import z3
import json
import torch
from Doping.pytorchtreelstm.treelstm import calculate_evaluation_orders
# from Doping.PySpacerSolver.utils import *
import os
import numpy as np
import glob
import argparse
import sys
import matplotlib.pyplot as plt
import logging
# def get_exp_name(prefix, exp_folder, vis, use_c, use_const_emb, use_dot_product, max_size, shuffle, negative_sampling_rate, threshold, dropout_rate):
def get_exp_name(configs, prefix = ""):
    '''
    construct a meaningful exp_name for the Tensorboard
    '''
    exp_name = [prefix]
    #exp_folder is in the form
    #"PySpacerSolver/MEDIA/backward_encoded_split_on_relu.smt2_250220_13_04_22/ind_gen_files/"
    # exp_name.append(exp_folder.split("/")[-3])
    for k in configs:
        if k in ["input_folders", "checkpoint"]: #do not put those parameters to the model name
            continue
        else:
            exp_name.append(configs[k][2])
            if isinstance(configs[k][0], bool):
                exp_name.append(str(int(configs[k][0])))
            else:
                exp_name.append(str(configs[k][0]))

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

def get_seed_file(seed_path):
    if seed_path is None:
        return None
    print("\t\tIn get seed file")
    seed_files = glob.glob(seed_path+"/pool_solver*.smt2")
    if(len(seed_files)==0):
        return None
    seed_files = sorted(seed_files)
    print(seed_files)
    seed_file = seed_files[0]
    return seed_file


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

def visualize_X(filename, key):
    with open(filename, "r") as f:
        data = json.load(f)[key]
        fig, ax = plt.subplots()
        im = ax.imshow(data)
        ax.set_title(filename)
        ax.set_xticks(np.arange(.5, len(data), 10))
        ax.set_yticks(np.arange(.5, len(data), 10))
        ax.set_xticklabels(np.arange(1, len(data), 10))
        ax.set_yticklabels(np.arange(1, len(data), 10))
        ax.grid(color='w', linestyle='-', linewidth=1)
        plt.show()

def parser_from_template(json_config_template = "/home/nle/workspace/Doping/exp_config_template.json"):
    with open(json_config_template, "r") as f:
        config_template = json.load(f)
    parser = argparse.ArgumentParser()
    for key in config_template:
        if key=="input_folders":
            continue
        long_name = key
        short_name = config_template[key][2]
        arg_type = type(config_template[key][0])
        help_text = config_template[key][1]
        if arg_type==bool:
            parser.add_argument("-{}".format(short_name),
                                "--{}".format(long_name),
                                default = None,
                                help = help_text,
                                action = 'store_true')
        else:
            parser.add_argument("-{}".format(short_name),
                                "--{}".format(long_name),
                                default = None,
                                type = arg_type,
                                help = help_text)
    return parser

def plot_to_tensorboard(writer, fig, step):
    """
    Takes a matplotlib figure handle and converts it using
    canvas and string-casts to a numpy array that can be
    visualized in TensorBoard using the add_image function

    Parameters:
        writer (tensorboard.SummaryWriter): TensorBoard SummaryWriter instance.
        fig (matplotlib.pyplot.fig): Matplotlib figure handle.
        step (int): counter usually specifying steps/epochs/time.
    """

    # Draw figure on canvas
    fig.canvas.draw()

    # Convert the figure to numpy array, read the pixel values and reshape the array
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # Normalize into 0-1 range for TensorBoard(X). Swap axes for newer versions where API expects colors in first dim
    img = img / 255.0
    # img = np.swapaxes(img, 0, 2) # if your TensorFlow + TensorBoard version are >= 1.8

    # Add figure in numpy "image" to TensorBoard writer
    writer.add_image('confusion_matrix', img, step)
    plt.close(fig)


def create_logger(lvl, name, outstream = 'stderr'):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, lvl))
    formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
    if outstream == 'stderr':
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
