import torch
import torch.nn as nn
from X_model import Model
from Doping.utils.X_Dataset import DataObj
import argparse
import json
import Doping.utils.utils as Du
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def setup_model(model_path):
    checkpoint = torch.load(model_path)
    model_metadata = checkpoint['metadata']
    dataset_metadata = checkpoint['dataset']
    print("I was trained with the configs:\n{}".format(json.dumps(checkpoint["configs"], indent=2)))
    print("Epoch", checkpoint["epoch"])
    
    model = Model(dataset_metadata['vocab_size'],
                  dataset_metadata['sort_size'],
                  emb_dim = model_metadata['emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                  const_emb_dim = model_metadata['const_emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                  tree_dim = model_metadata['tree_dim'],
                  use_const_emb = model_metadata['use_const_emb'],
                  use_dot_product = model_metadata['use_dot_product'],
                  device = torch.device('cuda')).eval()

    model.load_state_dict(checkpoint["model_state_dict"])

    return model

def load_configs_from_model(model_path):
    checkpoint = torch.load(model_path)
    configs = checkpoint['configs']
    return configs

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
    parser = Du.parser_from_template()
    parser.add_argument("--test_folder", help = "path to the test ind_gen_files folder", required = True)
    parser.add_argument("--model_path", help = "path to the .pt file", required = True)
    args = parser.parse_args()


    model_path = args.model_path
    model = setup_model(model_path)
    #load config
    configs = load_configs_from_model(model_path)
    #overwrite configs with parser value if user provide input
    for key,value in vars(args).items():
        if value is None or key not in configs:
            continue
        else:
            print("Setting {} in configs to {}".format(key, value))
            configs[key][0] = value

    dataObj = DataObj(args.test_folder,
                      max_size = configs["max_size"][0],
                      shuffle = configs["shuffle"][0],
                      train_size = 1,
                      threshold = configs["threshold"][0],
                      negative=configs["train_negative_model"][0])

    evaluate(model, dataObj, dataObj.train_P, configs["test_batch_size"][0])
