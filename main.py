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

dataObj = DataObj("/home/nv3le/workspace/Doping/PySpacerSolver/Exp55/ind_gen_files")
train = dataObj.train
test = dataObj.test
vocab = dataObj.vocab

def evaluate(model, testset):
    output = model(
        testset["C_batch"],
        testset["L_a_batch"],
        testset["L_b_batch"]
    ).cpu()
    true_label = testset["label_batch"].cpu()
    print("true:", testset["label_batch"])
    # print("output:", output)
    values, pred = torch.max(output, 1)
    print("pred:", pred)
    acc = accuracy_score(true_label, pred)
    print(confusion_matrix(true_label, pred))
    print("accurarcy", acc)
if __name__ == '__main__':
    model = Model(vocab['size'], emb_dim = 20, tree_dim = 20).train()
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
            evaluate(model, train)
            print("testing eval----------------------------")
            evaluate(model, test)
