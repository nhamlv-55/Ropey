import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
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

SWRITER = SummaryWriter()

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

    return acc
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', help='path to the ind_gen_files folder')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    parser.add_argument('-vis', action='store_true')
    args = parser.parse_args()

    exp_folder = args.input
    vis = args.vis
    dataObj = DataObj(exp_folder, max_size = 4000, train_size = 0.8, batch_size = 1024)
    test = dataObj.test
    vocab = dataObj.vocab

    print("DATASET SIZE:", dataObj.size())
    print("TEST SIZE:", dataObj.test["size"])
    model = Model(vocab['size'],
                  vocab['sort_size'],
                  emb_dim = 20,
                  tree_dim = 200,
                  out_dim =2,
                  use_c = True,
                  use_const_emb = False).train()
    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())

    for n in range(100):
        last_batch = False
        total_loss = 0

        while not last_batch:
            optimizer.zero_grad()
            loss = 0
            train, last_batch = dataObj.next_batch(dataObj.train_dps, "train")
            # print("Training with %d datapoints"%train["size"])
            output = model(
                train["C_batch"],
                train["L_a_batch"],
                train["L_b_batch"]
            )
            loss = loss_function(output, train["label_batch"])
            total_loss += loss

            loss.backward()
            optimizer.step()

        accurary = evaluate(model, test, vis)
        SWRITER.add_scalar('Loss/train', total_loss, n)
        SWRITER.add_scalar('Accuracy/test', accurary, n)        #empty gpu
        # torch.cuda.empty_cache()

        if n%10==0:
            # print(output.shape)
            print(f'Iteration {n+1} Loss: {loss}')
            #check that embedding is being trained
            print(model.emb(torch.LongTensor([5]).to(device = torch.device('cuda') ) ) )
            print("training eval---------------------------")
            # train = dataObj.train
            # evaluate(model, train, vis)
            print("testing eval----------------------------")
            print("TEST SIZE:", dataObj.test["size"])
            evaluate(model, test, vis)
