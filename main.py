import torch
import torch.nn as nn
import z3
from Doping.pytorchtreelstm.treelstm import TreeLSTM, calculate_evaluation_orders
import Doping.utils.utils as Du
from Doping.utils.Dataset import DataObj
from model import Model
import json
import os
from sklearn.metrics import confusion_matrix, accuracy_score
from termcolor import colored
import argparse
def evaluate(model, testset, vis = False):
    output = model(
        testset["C_batch"],
        testset["L_a_batch"],
        testset["L_b_batch"]
    ).cpu()
    true_label = testset["label_batch"].cpu()
    # print("true:", testset["label_batch"])
    m = nn.Softmax(dim = 1)
    # print("output:", output)
    values, pred = torch.max(m(output), 1)

    # print("pred:", pred)
    acc = accuracy_score(true_label, pred)
    print(confusion_matrix(true_label, pred))
    print("accurarcy", acc)

    true_label = true_label.tolist()
    values = values.tolist()
    pred = pred.tolist()
    if vis:
        print("Label\tPred\tConfidence")
        for i in range(len(pred)):
            if true_label[i]!=pred[i]:
                print(colored("%d\t%d\t%f"%(true_label[i], pred[i], values[i]), 'red'))
            else:
                print(colored("%d\t%d\t%f"%(true_label[i], pred[i], values[i]), 'green'))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', help='path to the ind_gen_files folder')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    parser.add_argument('-vis', action='store_true')
    args = parser.parse_args()

    exp_folder = args.input
    vis = args.vis
    dataObj = DataObj(exp_folder)
    train = dataObj.train
    test = dataObj.test
    vocab = dataObj.vocab


    model = Model(vocab['size'], vocab['sort_size'], emb_dim = 32, tree_dim = 200, out_dim =2).train()
    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())
    print("Training with %d datapoints"%train["size"])
    for n in range(1000):
        optimizer.zero_grad()
        loss = 0
        output = model(
            train["C_batch"],
            train["L_a_batch"],
            train["L_b_batch"]
        )
        loss = loss_function(output, train["label_batch"])
        loss.backward()
        optimizer.step()

        if n%100==0:
            # print(output.shape)
            print(f'Iteration {n+1} Loss: {loss}')
            #check that embedding is being trained
            print(model.emb(torch.LongTensor([5]).to(device = torch.device('cuda') ) ) )
            print("training eval---------------------------")
            evaluate(model, train, vis)
            print("testing eval----------------------------")
            evaluate(model, test, vis)
