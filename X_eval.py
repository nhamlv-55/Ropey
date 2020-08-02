import torch
import torch.nn as nn
from X_model import Model
from Doping.utils.X_Dataset import DataObj
import argparse

import Doping.utils.utils as Du
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def setup_model(model_path):
    checkpoint = torch.load(model_path)
    model_metadata = checkpoint['metadata']
    dataset_metadata = checkpoint['dataset']
    print("Epoch", checkpoint["epoch"])

    model = Model(dataset_metadata['vocab_size'],
                  dataset_metadata['sort_size'],
                  emb_dim = model_metadata['emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                  const_emb_dim = model_metadata['const_emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                  tree_dim = 100,
                  use_const_emb = model_metadata['use_const_emb'],
                  use_dot_product = model_metadata['use_dot_product'],
                  device = torch.device('cpu')).eval()

    model.load_state_dict(checkpoint["model_state_dict"])

    return model

def evaluate(model, dataObj, testset, test_bsz, examples_idx = None, writer = None, n = None ):
    #switch to eval mode

    model.eval()
    last_batch = False

    all_true_labels = []
    all_preds  = []
    all_values = []

    results = {"acc": -1,
               "pre": -1,
               "rec": -1,
               "f1": -1}

    while not last_batch:
        test, last_batch = dataObj.next_batch(testset, test_bsz, -1) #set negative_sampling_rate to -1 in evaluation
        output = model(
            test["L_a_batch"],
            test["L_b_batch"]
        )[0]
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
        )[0]
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

    #switch back to train mode
    model.train()
    return results

if __name__=="__main__":
    torch.no_grad()
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', help='path to the .pt file')
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


    model_path = args.model_path
    model = setup_model(model_path)
    dataObj = DataObj(exp_folder, max_size = max_size, shuffle = shuffle, train_size = 1, threshold = threshold, negative=args.train_negative_model)
    evaluate(model, dataObj, dataObj.train_P, args.test_batch_size)
