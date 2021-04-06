import torch
import torch.nn as nn
from Doping.RNN_model import RNNModel
from Doping.utils.RNN_Dataset import DataObj
import argparse
import json
import Doping.utils.utils as Du
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from enum import Enum

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

def setup_model(model_path):
    checkpoint = torch.load(model_path)
    model_metadata = checkpoint['metadata']['lemma_encoder']
    dataset_metadata = checkpoint['dataset']
    print("I was trained with the configs:\n{}".format(json.dumps(checkpoint["configs"], indent=2)))
    print("Epoch", checkpoint["epoch"])
    
    model = RNNModel(dataset_metadata['vocab_size'],
                     dataset_metadata['sort_size'],
                     emb_dim = model_metadata['emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                     const_emb_dim = model_metadata['const_emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                     tree_dim = model_metadata['tree_dim'],
                     use_const_emb = model_metadata['use_const_emb'],
                     use_dot_product = model_metadata['use_dot_product'],
                     device = torch.device('cuda')).eval()


    model.load_state_dict(checkpoint["model_state_dict"])

    return model

def plot_weight_tfboard(model, SWRITER, n):
    for name, weight in model.named_parameters():
        SWRITER.add_histogram(name,weight, n)
        if weight.grad is not None:
            SWRITER.add_histogram(f'{name}.grad',weight.grad, n)

        if len(list(weight.data.size()))==2:
            image = weight.data.cpu().detach().numpy()
            log.debug(image)
            image -= image.min()
            image /= image.max()
            log.debug(weight.data.size())
            log.debug(image)
            SWRITER.add_image("weight"+str(name), image, global_step = n,  dataformats='HW')




def plot_tsne(model, vocab, title, n=-1):
    #get emb
    raw_emb_w = model.lemma_encoder.emb.weight.detach().cpu().tolist()
    emb_w = []
    label = []
    for i in range(len(raw_emb_w)):
        if vocab["w_count"][str(i)]>1:
            emb_w.append(raw_emb_w[i])
            label.append(vocab["id2w"][str(i)])


    sort_emb_w = model.lemma_encoder.sort_emb.weight.detach().cpu()

    tsne = TSNE(2)
    tsne_proj = tsne.fit_transform(emb_w)

    sort_tsne = TSNE(2)
    sort_tsne_proj = sort_tsne.fit_transform(sort_emb_w)

    fig, axs = plt.subplots(2,2, figsize=(20,20))

    axs[0][1].set_xlim(-4,4)
    axs[0][1].set_ylim(-4,4)

    axs[1][1].set_xlim(-4,4)
    axs[1][1].set_ylim(-4,4)




    fig.suptitle(title)

    #plot token emb
    for indices in range(len(emb_w)):
        axs[0][0].scatter(tsne_proj[indices,0],tsne_proj[indices,1], c = 'blue')
        axs[0][1].scatter(emb_w[indices][0], emb_w[indices][1], c = 'green')
    for indices in range(len(emb_w)):
        axs[0][0].annotate(label[indices], 
                        (tsne_proj[indices,0],tsne_proj[indices,1] ), 
                        size=5)
        axs[0][1].annotate(label[indices], 
                           (emb_w[indices][0], emb_w[indices][1]),
                        size=5)

    #plot sort emb
    for indices in range(sort_emb_w.shape[0]):
        axs[1][0].scatter(sort_tsne_proj[indices,0],sort_tsne_proj[indices,1], c = 'red')

        axs[1][1].scatter(sort_emb_w[indices][0], sort_emb_w[indices][1], c = 'brown')
    for indices in range(sort_emb_w.shape[0]):
        axs[1][0].annotate(vocab["id2s"][str(indices)], 
                        (sort_tsne_proj[indices,0], sort_tsne_proj[indices,1] ), 
                        size = 5)
        axs[1][1].annotate(vocab["id2s"][str(indices)], 
                           (sort_emb_w[indices][0], sort_emb_w[indices][1]),
                        size=5)

    fig.savefig('tsne_emb_{}.svg'.format(n))


def load_configs_from_model(model_path):
    checkpoint = torch.load(model_path)
    configs = checkpoint['configs']
    return configs

def print_debug(test, values, pred):
    pass
    true_label = test["labels"][0].cpu()
    pred = pred.tolist()
    values = values.tolist()
    assert(len(true_label) == len(pred))
    return



def evaluate(model, dataObj, datapart, test_bsz, writer = None, n = None, debug = False, examples_idx = None):
    class CHK_LEMMA_RES(Enum):
        perfect = 1
        eligable = 2 #if the only mistake is that we keep literal that should be dropped
        wrong = 3 #if we drop literal that cannot be drop

    def check_lemma(test, pred, counters):
        true_label = test["labels"][0].cpu()
        pred = pred.tolist()
        perfect = True
        for idx in range(len(true_label)):
            if true_label[idx] == 1 and pred[idx]==0:
                counters["wrong_cnt"]+=1
                counters["wrong_len"]+=len(true_label)
                return CHK_LEMMA_RES.wrong
            if true_label[idx] == 0 and pred[idx]==1:
                perfect = False

        if perfect:
            counters["perfect_cnt"]+=1
            counters["perfect_len"]+=len(true_label)
            return CHK_LEMMA_RES.perfect
        else:
            counters["eligable_cnt"]+=1
            counters["eligable_len"]+=len(true_label)
            return CHK_LEMMA_RES.eligable


    #switch to eval mode
    model.eval()
    last_batch = False

    all_true_labels = []
    all_preds  = []
    all_values = []

    counters = {"wrong_cnt": 0, "perfect_cnt": 0, "eligable_cnt": 0,
                "wrong_len": 0, "perfect_len": 0, "eligable_len": 0}


    results = {"acc": -1,
               "pre": -1,
               "rec": -1,
               "f1": -1}

    while not last_batch:
        test, last_batch = dataObj.next_batch(datapart, test_bsz, gamma = -1)
        if test is not None:
            labels = test["labels"][0]
            # print("labels", labels, labels.size())

            output = model(test["input_trees"][0])

            true_label = labels.cpu()
            m = nn.Softmax(dim = 1)

            values, pred = torch.max(m(output), 1)
            check_lemma(test, pred, counters)
            print_debug(test, values, pred)
            # print("pred", pred)

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


    #compute average len
    if counters["perfect_cnt"]>0:
        counters["perfect_avg_len"] = counters["perfect_len"]/counters["perfect_cnt"]
    if counters["wrong_cnt"]>0:
        counters["wrong_avg_len"] = counters["wrong_len"]/counters["wrong_cnt"]
    if counters["eligable_cnt"]>0:
        counters["eligable_avg_len"] = counters["eligable_len"]/counters["eligable_cnt"]

    print("counters", json.dumps(counters, indent = 2))
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
                      negative=configs["train_negative_model"][0],
                      device = configs["device"][0])

    evaluate(model, dataObj, dataObj.train_P, configs["test_batch_size"][0])
