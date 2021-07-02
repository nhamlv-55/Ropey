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
import os
import glob
from pathlib import Path
import traceback
from datetime import datetime
import mysql.connector
from Doping.cred import cred
def oJson(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data


def setup_model(model_path, log_level = "INFO"):
    checkpoint = torch.load(model_path)
    model_metadata = checkpoint['metadata']['lemma_encoder']
    dataset_metadata = checkpoint['dataset']
    print("I was trained with the configs:\n{}".format(json.dumps(checkpoint["configs"], indent=2)))
    print("Epoch", checkpoint["epoch"])

    if 'use_var_emb' in model_metadata:
        use_var_emb = model_metadata['use_var_emb']
    else:
        use_var_emb = True

    model = RNNModel(dataset_metadata['vocab_size'],
                     dataset_metadata['sort_size'],
                     emb_dim = model_metadata['emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                     const_emb_dim = model_metadata['const_emb_dim'], #30 is the max emb_dim possible, due to the legacy dataset
                     pos_emb_dim=model_metadata['pos_emb_dim'],
                     tree_dim = model_metadata['tree_dim'],
                     device = torch.device('cuda'),
                     log_level = log_level,
                     use_var_emb = use_var_emb).eval()


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
    dataset_metadata = checkpoint['dataset']
    return configs, dataset_metadata

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
    print("accuracy", acc)
    print("f1", f1)
    print("precision", pre)
    print("recall", recall)


    #compute average len
    counters["perfect_avg_len"] = counters["perfect_len"]/counters["perfect_cnt"] if counters["perfect_cnt"]>0 else -1
    counters["wrong_avg_len"] = counters["wrong_len"]/counters["wrong_cnt"] if counters["wrong_cnt"]>0 else -1
    counters["eligable_avg_len"] = counters["eligable_len"]/counters["eligable_cnt"] if counters["eligable_cnt"]>0 else -1
    cnt  = (counters["perfect_cnt"] + counters["wrong_cnt"] + counters["eligable_cnt"])
    counters["perfect_ratio"] = counters["perfect_cnt"]/cnt
    counters["wrong_ratio"] = counters["wrong_cnt"]/cnt
    counters["eligable_ratio"] = counters["eligable_cnt"]/cnt
    results["counters"] = counters

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

def get_lustre_variants(test_folder, get_random_v = False):
    """
    Given a test_folder of the form /home/nle/workspace/Doping/benchmarks/vmt-chc-benchmarks/lustre/SYNAPSE_1.smt2/ind_gen_file,
    this function will first extract the SYNAPSE_1.smt2 part,
    then find all variants of the form /home/nle/workspace/Doping/benchmarks/vmt-chc-benchmarks/lustre/SYNAPSE_1_*.smt2,
    as well as all variants of the form /home/nle/workspace/Doping/benchmarks/vmt-chc-benchmarks/lustre/SYNAPSE_1.smt2/variant_*/input_file.smt2
    """
    exp_folder = test_folder.parent.absolute()
    all_exp_folder = exp_folder.parent.absolute()
    exp_seed_name = Path(exp_folder).parts[-1]

    assert(".smt2.folder" in exp_seed_name)

    exp_seed_name = exp_seed_name.replace(".smt2.folder", "")

    query = str(all_exp_folder)+"/"+exp_seed_name+"_*.smt2.folder"

    variants = glob.glob(query)

    variants.append(str(exp_folder))
    """
    if we want to measure random variants created by permuting constants, set get_random_v to True
    """
    if get_random_v:
        for i in range(10):
            variants.append(str(exp_folder.joinpath("variant_{}".format(i))))
    return variants

def get_model_path(test_folder, n = 299, tag = ""):
    model_folder = str(test_folder.parent.absolute().joinpath("models"))
    suffix = "{}.pt".format(n)

    all_models = glob.glob(model_folder+"/{}*.pt".format(tag))
    all_models.sort(key = os.path.getmtime, reverse = True)
    for model_path in all_models:
        if model_path.endswith(suffix):
            
            return model_path
    return None

def get_db_conn():
    db = mysql.connector.connect(
        host='localhost',
        database = "Dopey",
        user = cred["username"],
        password = cred["password"]
    )
    return db

if __name__=="__main__":
    parser = Du.parser_from_template()
    parser.add_argument("--test_folder", help = "path to the test ind_gen_files folder", required = True)
    parser.add_argument("--variants_file", help = "Optional. If provided, will test the model againsts instances listed in the file", required = False)

    parser.add_argument("--model_tag", default = "", help = "Optional. If provided, will find the model that has the tag", required = False)
    args = parser.parse_args()

    test_folder = Path(args.test_folder)
    exp_folder = test_folder.parent.absolute()
    if args.variants_file is None:
        variants = get_lustre_variants(test_folder)
    else:
        variants = open(args.variants_file, "r").read().split("\n")
    
    model_path  = get_model_path(test_folder, n = 'ES', tag = args.model_tag)
    if model_path is None:
        model_path  = get_model_path(test_folder, n = 1499, tag = args.model_tag)
    print("Eval model\n", model_path)
    #load vocab
    vocab = json.load(open(os.path.join(test_folder, "vocab.json")))
    #load model
    model  = setup_model(model_path)
    #load configs
    configs, dataset_metadata = load_configs_from_model(model_path)

    results = {"model": model_path}

    db = get_db_conn()
    c = db.cursor()

    #evaluate variants
    if dataset_metadata["train_portion"]==1:
        print("train_portion = 1.0-> We are evaluating transfered models. Start evaluating variants...")
        for v in variants:
            try:
                print("Evaluating on ", v)
                v_path = os.path.join(v, "ind_gen_files")


                var_dataObj = DataObj(v_path,
                                    max_size = dataset_metadata["max_size"],
                                    shuffle = dataset_metadata["shuffle"],
                                    train_size = dataset_metadata["train_portion"],
                                    threshold = dataset_metadata["threshold"],
                                    device = configs["device"][0])
                print(len(var_dataObj.train_dps))
                results[v] = evaluate(model, var_dataObj, var_dataObj.train_dps, 1, debug=True)
                r = results[v]["counters"]
                c.execute('''
                REPLACE INTO Dopey.Dopey_RNN_Res
                (model_path, variant, seed, wrong_cnt, perfect_cnt, eligable_cnt, perfect_ratio, wrong_ratio, eligable_ratio, perfect_avg_len, wrong_avg_len, eligable_avg_len)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                ''', (os.path.basename(model_path),
                      str(Path(v).parts[-2:]) if "variant" in v else str(Path(v).parts[-1]),
                      str(exp_folder.parts[-1]),
                      r["wrong_cnt"], r["perfect_cnt"], r["eligable_cnt"],
                      r["perfect_ratio"], r["wrong_ratio"], r["eligable_ratio"],
                      r["perfect_avg_len"], r["wrong_avg_len"], r["eligable_avg_len"]))
            except:
                print(c.statement)
                traceback.print_exc()
            db.commit()
    else:
        #evaluate test set
        print("train_portion < 1.0-> We are evaluating online mode. Start evaluating on test set...")
        try:
            v = str(test_folder.parent.absolute())
            print("Evaluating on ", v)
            v_path = os.path.join(v, "ind_gen_files")


            var_dataObj = DataObj(v_path,
                                max_size = dataset_metadata["max_size"],
                                shuffle = dataset_metadata["shuffle"],
                                train_size = dataset_metadata["train_portion"],
                                threshold = dataset_metadata["threshold"],
                                device = configs["device"][0])
            results[v+".testset"] = evaluate(model, var_dataObj, var_dataObj.test_dps, 1, debug=True)
            r = results[v+".testset"]["counters"]
            c.execute('''
            REPLACE INTO Dopey.Dopey_RNN_Res
            (model_path, variant, seed, wrong_cnt, perfect_cnt, eligable_cnt, perfect_ratio, wrong_ratio, eligable_ratio, perfect_avg_len, wrong_avg_len, eligable_avg_len)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (os.path.basename(model_path),
                  str(Path(v).parts[-1])+".testset",
                  str(exp_folder.parts[-1])+".testset",
                  r["wrong_cnt"], r["perfect_cnt"], r["eligable_cnt"],
                  r["perfect_ratio"], r["wrong_ratio"], r["eligable_ratio"],
                  r["perfect_avg_len"], r["wrong_avg_len"], r["eligable_avg_len"]))
        except:
            print(c.statement)
            traceback.print_exc()

        db.commit()
    now = datetime.now()
    current_time = now.strftime("%d%m_%H_%M_%S")
    with open("RESULTS_{}.json".format(current_time), "w") as f:
        json.dump(results, f, indent = 2)

