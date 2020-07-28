import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
import z3
from Doping.pytorchtreelstm.treelstm import TreeLSTM, calculate_evaluation_orders
import Doping.utils.utils as Du
from Doping.utils.X_Dataset import DataObj
from Doping.settings import MODEL_PATH, new_model_path
from X_model import Model
import json
import os
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from termcolor import colored
import argparse
import random
import logging

#TRAIN_BSZ could be much bigger than TEST_BSZ because we use negative sampling in training
TRAIN_BSZ = 200
TEST_BSZ = 70


def evaluate(model, testset, examples_idx = None, writer = None, n = None ):
    last_batch = False

    all_true_labels = []
    all_preds  = []
    all_values = []

    results = {"acc": -1,
               "pre": -1,
               "rec": -1,
               "f1": -1}

    while not last_batch:
        test, last_batch = dataObj.next_batch(testset, TEST_BSZ, -1) #set negative_sampling_rate to -1 in evaluation
        output = model(
            test["L_a_batch"],
            test["L_b_batch"]
        )
        true_label = test["label_batch"].cpu()
        m = nn.Softmax(dim = 1)

        values, pred = torch.max(m(output), 1)

        all_true_labels.extend(true_label.tolist())
        all_preds.extend(pred.tolist())
        all_values.extend(values.tolist())

    acc = accuracy_score(all_true_labels, all_preds)
    f1 = f1_score(all_true_labels, all_preds)
    pre = precision_score(all_true_labels, all_preds)
    recall = recall_score(all_true_labels, all_preds)

    results["acc"] = acc
    results["f1"] = f1
    results["pre"] = pre
    results["rec"] = recall

    print(confusion_matrix(all_true_labels, all_preds)) 
    print("accurarcy", acc)
    print("f1", f1)
    print("precision", pre)
    print("recall", recall)
    true_label = true_label.tolist()
    values = values.tolist()
    pred = pred.tolist()
    if examples_idx is not None:
        #grab the random 20 examples
        examples_dps = [testset[i] for i in examples_idx]
        test, last_batch = dataObj.next_batch(examples_dps, -1, -1)
        output = model(
            test["C_batch"],
            test["L_a_batch"],
            test["L_b_batch"]
        )
        true_label = test["label_batch"].cpu()
        m = nn.Softmax(dim = 1)

        values, pred = torch.max(m(output), 1)

        true_label = true_label.tolist()
        pred = pred.tolist()
        values = values.tolist()

        for idx in range(len(examples_dps)):
            example = examples_dps[idx]
            display_text = Du.display_example(example, true_label[idx], pred[idx], values[idx])
            
            writer.add_text('example', display_text, n)
    return results
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', help='path to the ind_gen_files folder')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    parser.add_argument('-v', '--vis', action='store_true')
    parser.add_argument('-C', '--use_c', action='store_true')
    parser.add_argument('-D', '--use_dot_product', action='store_true')
    parser.add_argument('-E', '--use_const_emb', action='store_true')
    parser.add_argument('-M', '--max_size', type = int, default = -1)
    parser.add_argument('--train_batch_size', type = int, default = 200)
    parser.add_argument('--test_batch_size', type = int, default = 70)
    parser.add_argument('-Nr', '--negative_sampling_rate', type = int, default = -1, help="controlling how many negative samples are used per 1 positive sample")
    parser.add_argument('-S', '--shuffle', action='store_true')
    parser.add_argument('--train_negative_model', action='store_true')
    parser.add_argument('-N', '--epoch', type = int, default = 100)
    parser.add_argument('--eval_epoch', type = int, default = 10)
    parser.add_argument('--save_epoch', type = int, default = 100)
    parser.add_argument('-th','--threshold', type = float, default = 0.75, help="Cap all entries in the matrix that greater than the threshold to be 1, 0 otherwise")
    parser.add_argument('-p','--prefix', default = "model", help="Prefix for the model name. Default is just `model`")
    args = parser.parse_args()

    exp_folder = args.input
    vis = args.vis
    use_c = args.use_c
    use_const_emb = args.use_const_emb
    use_dot_product = args.use_dot_product
    max_size = args.max_size
    shuffle = args.shuffle
    n_epoch = args.epoch
    eval_epoch = args.eval_epoch
    save_epoch = args.save_epoch
    threshold = args.threshold
    negative_sampling_rate = args.negative_sampling_rate
    prefix = args.prefix

    TRAIN_BSZ = args.train_batch_size
    TEST_BSZ  = args.test_batch_size

    exp_name = Du.get_exp_name(prefix, exp_folder, vis, use_c, use_const_emb, use_dot_product, max_size, shuffle, negative_sampling_rate, threshold)
    SWRITER = SummaryWriter(comment = exp_name)
    #NOTE: batch_size should not be a divisor of the number of dps in train set or test set (batch_size = 32 while train has 4000 is not good)
    dataObj = DataObj(exp_folder, max_size = max_size, shuffle = shuffle, train_size = 1, threshold = threshold, negative=args.train_negative_model)
    vocab = dataObj.vocab
    device = torch.device('cuda')
    print("DATASET SIZE:", dataObj.size)
    print("NEGATIVE SAMPLING RATE:", negative_sampling_rate)
    # print("TRAIN SIZE:", dataObj.train["size"])
    # print("TEST SIZE:", dataObj.test["size"])
    model = Model(vocab['size'],
                  vocab['sort_size'],
                  emb_dim = 20, #30 is the max emb_dim possible, due to the legacy dataset
                  const_emb_dim = vocab["const_emb_size"],
                  tree_dim = 100,
                  use_const_emb = use_const_emb,
                  use_dot_product = use_dot_product,
                  device = device).train()
    loss_function = torch.nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.Adam(model.parameters())

    metadata = {"dataset": dataObj.metadata(), "model": model.metadata()}
    SWRITER.add_text('metadata', json.dumps(metadata, indent = 2)  )
    # examples_idx = random.sample(list(range(len(dataObj.test_dps))), 20)
    for n in range(n_epoch):
        last_batch = False
        total_loss = 0

        while not last_batch:
            optimizer.zero_grad()
            loss = 0
            train, last_batch = dataObj.next_batch(dataObj.train_P , batch_size = TRAIN_BSZ, negative_sampling_rate = negative_sampling_rate)
            # print(last_batch)
            # print("Training with %d datapoints"%train["size"])
            output = model(
                train["L_a_batch"],
                train["L_b_batch"]
            )
            loss = loss_function(output, train["label_batch"].to(device))
            total_loss += loss

            loss.backward()
            optimizer.step()

        # torch.cuda.empty_cache()

        if n%eval_epoch==0:
            # print(output.shape)
            train_res = evaluate(model, dataObj.train_P)
            # print("example_ids:", examples_idx)
            # test_res = evaluate(model, dataObj.test_P)
            SWRITER.add_scalar('Loss/train', total_loss, n)
            SWRITER.add_scalar('Accuracy/train', train_res["acc"], n)
            # SWRITER.add_scalar('Accuracy/test', test_res["acc"], n)
            SWRITER.add_scalar('F1/train', train_res["f1"], n)
            # SWRITER.add_scalar('F1/test', test_res["f1"], n)
            print(f'Iteration {n+1} Loss: {loss}')
            #check that embedding is being trained
            # print(model.emb(torch.LongTensor([5]).to(device = device ) ) )

        if n%save_epoch==0 or n==n_epoch - 1:
            model_path = new_model_path(basename = exp_name)
            print("Saving to ", model_path)
            torch.save({
                'epoch': n,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
                'dataset': dataObj.metadata(),
                'metadata': model.metadata()
            }, model_path)
