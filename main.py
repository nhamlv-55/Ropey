import torch
import torch.nn as nn
import z3
from Doping.pytorchtreelstm.treelstm import TreeLSTM, calculate_evaluation_orders

from Doping.pytorchtreelstm.treelstm import batch_tree_input
import Doping.utils.utils as Du
from model import Model
import glob
import json
import os
C_trees = []
L_a_trees = []
L_b_trees = []
labels = []

datafolder = "PySpacerSolver/Exp2/ind_gen_files/"
all_dps = glob.glob(datafolder+"/*.dp.json")
for dp in all_dps:
    with open(dp, "r") as f:
        data  = json.load(f)
        C_trees.append(Du.convert_tree_to_tensors(data["C_tree"]))
        L_a_trees.append(Du.convert_tree_to_tensors(data["L_a_tree"]))
        L_b_trees.append(Du.convert_tree_to_tensors(data["L_b_tree"]))
        labels.append(data["label"])

C_batch = batch_tree_input(C_trees)
print("C_batch_size", C_batch)
L_a_batch = batch_tree_input(L_a_trees)
L_b_batch = batch_tree_input(L_b_trees)
label_batch = torch.tensor(labels)
vocab_file = os.path.join(datafolder, "vocab.json")
with open(vocab_file, "r") as f:
    vocab = json.load(f)

if __name__ == '__main__':
    model = Model(vocab['size']).train()
    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())

    for n in range(1000):
        optimizer.zero_grad()
        loss = 0
        output = model(
            C_batch,
            L_a_batch,
            L_b_batch
        )
        loss = loss_function(output, label_batch)
        loss.backward()
        optimizer.step()

        if n%100==0:
            # print(output.shape)
            print(f'Iteration {n+1} Loss: {loss}')
            #check that embedding is being trained
            print(model.emb(torch.LongTensor([5])))
