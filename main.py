import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
import z3
from Doping.pytorchtreelstm.treelstm import TreeLSTM, calculate_evaluation_orders
import Doping.utils.utils as Du
from Doping.utils.Dataset import DataObj
from Doping.settings import MODEL_PATH, new_model_path
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
    parser.add_argument('-v', '--vis', action='store_true')
    parser.add_argument('-C', '--use_c', action='store_true')
    parser.add_argument('-E', '--use_const_emb', action='store_true')
    parser.add_argument('-M', '--max_size', type = int, default = -1)
    parser.add_argument('-S', '--shuffle', action='store_true')
    parser.add_argument('-N', '--epoch', type = int, default = 300)
    parser.add_argument('--eval-epoch', type = int, default = 10)
    parser.add_argument('--save-epoch', type = int, default = 100)
    args = parser.parse_args()

    exp_folder = args.input
    vis = args.vis
    use_c = args.use_c
    use_const_emb = args.use_const_emb
    max_size = args.max_size
    shuffle = args.shuffle
    n_epoch = args.epoch
    eval_epoch = args.eval_epoch
    save_epoch = args.save_epoch

    dataObj = DataObj(exp_folder, max_size = max_size, shuffle = shuffle, train_size = 0.8, batch_size = 1024)
    test = dataObj.test
    vocab = dataObj.vocab

    print("DATASET SIZE:", dataObj.size())
    print("TRAIN SIZE:", dataObj.train["size"])
    print("TEST SIZE:", dataObj.test["size"])
    model = Model(vocab['size'],
                  vocab['sort_size'],
                  emb_dim = 20,
                  tree_dim = 200,
                  out_dim =2,
                  use_c = use_c,
                  use_const_emb = use_const_emb).train()
    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())

    metadata = {"dataset": dataObj.metadata(), "model": model.metadata()}
    SWRITER.add_text('metadata', json.dumps(metadata, indent = 2)  )
    for n in range(n_epoch):
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

        if n%eval_epoch==0:
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

        if n%save_epoch==0:
            model_path = new_model_path()
            print("Saving to ", model_path)
            torch.save({
                'epoch': n,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
                'dataset': dataObj.metadata(),
                'metadata': model.metadata()
            }, model_path)
