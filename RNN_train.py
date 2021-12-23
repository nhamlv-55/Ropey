import torch
from torch.utils.tensorboard import SummaryWriter
from Doping.pytorchtreelstm.treelstm import TreeLSTM, calculate_evaluation_orders
from Doping.utils.RNN_Dataset import DataObj
from Doping.settings import MODEL_PATH, new_model_path
from RNN_model import RNNModel
import json
import os
from termcolor import colored
import argparse
import random
import logging
from tqdm import tqdm
import matplotlib.pyplot as plt
import Doping.utils.utils as Du
from Doping.RNN_eval import evaluate, plot_tsne, plot_weight_tfboard

PRETRAIN_EPC = 100 #turn off the token emb for how many iterations?
EARLY_STOPPING_COUNT = 5
def save_model(model_path, model, optimizer, dataObj):
    print("Saving to ", model_path)
    torch.save({
        'model_path': model_path,
        'epoch': n,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
        'dataset': dataObj.metadata(),
        'metadata': model.metadata(),
        'configs': configs,
        'no_of_params': no_of_params
    }, model_path)

if __name__ == '__main__':
    parser = Du.parser_from_template()
    parser.add_argument("--json_config_file", "-JI", required=True, help="Path to the json config")
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    args = parser.parse_args()
    log = Du.create_logger(args.logLevel, __name__)
    #load the config file
    with open(args.json_config_file, "r") as f:
        configs = json.load(f)

    #overwrite configs with parser value if user provide input
    for key,value in vars(args).items():
        if value is None or key not in configs:
            continue
        else:
            print("Setting {} in configs to {}".format(key, value))
            configs[key][0] = value

    exp_name = Du.get_exp_name(configs, prefix="NoConstEmb")
    SWRITER = SummaryWriter(comment = exp_name)
    print("Configs:\n", json.dumps(configs, indent=2))
    dataObjs = []
    vocabs = []
    device = torch.device(configs['device'][0])
    for exp_folder in configs["input_folders"]:
        if os.path.exists(exp_folder):
            dataObj = DataObj(exp_folder,
                            device = device,
                            max_size = configs["max_size"][0],
                            shuffle = configs["shuffle"][0],
                            train_size = configs["train_portion"][0],
                            threshold = configs["threshold"][0],
                            )
            vocab = dataObj.vocab

            dataObjs.append(dataObj)
            vocabs.append(vocab)
        else:
            log.info("exp_folder {} doesnt exist".format(exp_folder))
    model = RNNModel(vocabs[0]['size'],
                     vocabs[0]['sort_size'],
                     emb_dim = configs['emb_dim'][0],
                     # const_emb_dim = vocabs[0]["const_emb_size"],
                     const_emb_dim = 0,
                     pos_emb_dim=configs['pos_emb_dim'][0],
                     tree_dim = configs['tree_dim'][0],
                     dropout_rate = configs["dropout_rate"][0],
                     device = device,
                     log_level = "INFO",
                     use_var_emb = configs["use_const_emb"][0]).train()

    no_of_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print("no_of_params:", no_of_params)
    if configs["checkpoint"][0]!="":
        print("Training start from this checkpoint:\n{}".format(configs["checkpoint"][0]))
        checkpoint = torch.load(configs["checkpoint"][0])
        model.load_state_dict(checkpoint["model_state_dict"])


    
    loss_function = torch.nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.Adam(model.parameters())

    metadata = {"dataset": dataObj.metadata(), "model": model.metadata(), "configs": configs, "no_of_params": no_of_params}
    SWRITER.add_text('metadata', json.dumps(metadata, indent = 2)  )
    # examples_idx = random.sample(list(range(len(dataObj.test_dps))), 20)
    model_path = new_model_path(basename = exp_name, epoch = "RN")
    plot_tsne(model, vocabs[0], model_path, "RN")
    counter = 0 #use for early stopping. If in train set we reach good performance > EARLY_STOPPING_COUNT, we stop the training
    try:
        with tqdm(range(configs["epoch"][0])) as progress_bar:
            for n in range(configs["epoch"][0]):
                if n < PRETRAIN_EPC:
                    model.disable_token_emb()
                    model.disable_constant_emb()
                else:
                    model.enable_token_emb()
                    model.enable_constant_emb()


                for dataObj in dataObjs:
                    last_batch = False
                    n_dps = 0
                    optimizer.zero_grad()
                    total_loss = 0
                    while not last_batch:
                        train, last_batch = dataObj.next_batch(dataObj.train_dps, 1, configs['gamma'][0])

                        if train is not None:
                            labels = train["labels"][0]
                            # print("labels", labels, labels.size())

                            output = model(train["input_trees"][0])

                            loss = loss_function(output, labels)
                            total_loss += loss
                            n_dps+=1
                    total_loss.backward()
                    #clip the gradient
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 10)
                    optimizer.step()

                    if n%configs["eval_epoch"][0]==0:
                        print("Result using data from: {}".format(str(dataObj)))
                        # print(output.shape)
                        train_res = evaluate(model, dataObj, dataObj.train_dps, 1)
                        if train_res["counters"]["perfect_ratio"]>0.95:
                            counter+=1
                        else:
                            counter = 0 #reset counter
                        # print("example_ids:", examples_idx)
                        test_res = evaluate(model, dataObj, dataObj.test_dps, 1)

                        # plot_weight_tfboard(model, SWRITER, n)
                        SWRITER.add_scalar('Loss/train', total_loss, n)
                        SWRITER.add_scalar('Accuracy/train', train_res["acc"], n)
                        SWRITER.add_scalar('Accuracy/test', test_res["acc"], n)
                        SWRITER.add_scalar('F1/train', train_res["f1"], n)
                        SWRITER.add_scalar('F1/test', test_res["f1"], n)
                        print(f'Iteration {n+1} Loss: {total_loss}')
                        #check that embedding is being trained

                progress_bar.update(1)
                if n%configs["save_epoch"][0]==0 or n==configs["epoch"][0] - 1:
                    model_path = new_model_path(basename = exp_name, epoch = n)
                    save_model(model_path, model, optimizer, dataObj)
                    # plot_tsne(model, vocabs[0], model_path, n)
                elif counter == EARLY_STOPPING_COUNT:
                    model_path = new_model_path(basename = exp_name, epoch = "ES")
                    save_model(model_path, model, optimizer, dataObj)
                    print("Achieve good performance multiple times in a row. Early Stopping...")
                    exit(0)
    except KeyboardInterrupt:
        model_path = new_model_path(basename = exp_name, epoch="KI")
        print("Keyboard Interupted. Saving to ", model_path)
        save_model(model_path, model, optimizer, dataObj)
        plot_tsne(model, vocabs[0], model_path, n)
