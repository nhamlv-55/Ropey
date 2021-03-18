import Doping.PySpacerSolver.utils as DPu
from Doping.pytorchtreelstm.treelstm import batch_tree_input
import glob
import json
import torch
from sklearn.model_selection import train_test_split
import os
import random
import logging
from Doping.utils.utils import calculate_P

logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class DataObj:
    def __init__(self, datafolder, device, name = "dataset", shuffle = True, max_size = -1, train_size = 0.67, threshold = 0.75):
        '''
        datafolder: path to the /ind_gen_files folder
        name: name of the dataset
        shuffle: whether to shuffle the dataset. If this is set to False, the dataset will be ordered by the order in which the datapoints appear
        max_size: how many datapoints to use (test+ train). To test the performance after some certain spacer's checkpoints.
        batch_size: batch_size for training
        train_size: how much of the dataset is used for training
        '''
        self.datafolder = datafolder
        self.device = device
        self.all_dps = []
        self.size = 0
        self.max_size = max_size
        self.total_dps = 10000
        self.id2lits_json = {}
        self.lits_str2id = {}
        self.vocab = {}
        self.train_dps = []
        self.test_dps = []
        self.data_pointer = 0
        self.train_size = train_size
        self.shuffle = shuffle
        self.const_emb_size = 0
        self.X_test_filename = ""
        self.X_train_filename = ""
        self.rnn_dps = []
        self.train_P = None
        self.test_P = None
        self.threshold = threshold
        
        self.build_dataset()
        self.get_vocab()

    def metadata(self):
        return {"datafolder": self.datafolder,
                "size": self.size,
                "max_size": self.max_size,
                "train_size": self.train_size,
                "vocab_size": self.vocab['size'],
                "sort_size": self.vocab['sort_size'],
                "shuffle": self.shuffle,
                "threshold": self.threshold,
        }

    def get_vocab(self):
        vocab_file = os.path.join(self.datafolder, "vocab.json")
        with open(vocab_file, "r") as f:
            self.vocab = json.load(f)


    def get_lit_id(self, lit_str):
        if lit_str in self.lits_str2id:
            return self.lits_str2id[lit_str]
        else:
            return -1

    def query_train_p(self, lit_str_a, lit_str_b):
        lit_id_a = self.get_lit_id(lit_str_a)
        lit_id_b = self.get_lit_id(lit_str_b)

        if lit_id_a != -1 and lit_id_b != -1:
            return self.train_P[lit_id_a][lit_id_b]

    def build_dataset(self):
        self.datafolder = os.path.join(self.datafolder, "")
        self.lit_files = glob.glob(self.datafolder+"/negative_lit_*.json")
        self.lit_files = sorted(self.lit_files)
        self.size = len(self.lit_files)
        #pre convert all lit tree to tensors
        for lf in self.lit_files:
            with open(lf, "r") as f:
                lit = json.load(f)
                # print(lit)
                lit_index = lit["index"]
                assert(lit_index not in self.id2lits_json)
                lit_tree = DPu.convert_tree_to_tensors(lit["tree"], self.device)
                self.id2lits_json[lit_index] = {"lit_tree": lit_tree, "filename": lf}

        #load lits_map
        lits_maps = glob.glob(self.datafolder + "/negative_lits_map*.json")

        lits_maps = sorted(lits_maps)
        lits_map_file = lits_maps[-1]
        with open(lits_map_file, "r") as f:
            self.lits_str2id = json.load(f)

        #load RNN_datapoints
        rnn_dps = glob.glob(self.datafolder + "/RNN_datapoints*.json")
        rnn_dps = sorted(rnn_dps)
        with open(rnn_dps[-1], "r") as f:
            self.rnn_dps = json.load(f)["RNN_datapoints"]



    def next_batch(self, batch_size):
        last_batch = False
        dataset = {}
        input_trees = []
        labels = []
        log.debug("data_pointer:{}".format(self.data_pointer))
        log.debug(len(self.rnn_dps))

        for i in range(self.data_pointer, min(self.data_pointer + batch_size, len(self.rnn_dps))):
            #for each datapoint (timestamp, original cube, inducted cube, mask)
            datapoint = self.rnn_dps[i]

            lit_jsons = [self.id2lits_json[idx]["lit_tree"] for idx in datapoint["ori"]]

            ori_tree_input = batch_tree_input(lit_jsons)

            input_trees.append(ori_tree_input)
            labels.append(torch.tensor(datapoint["mask"]).to(self.device))

        if len(input_trees) == 0:
            self.data_pointer = 0
            return None, True


        dataset["size"] = len(input_trees)
        dataset["input_trees"] = input_trees
        dataset["labels"] = labels
        self.data_pointer+=batch_size
        if self.data_pointer>len(self.rnn_dps):
            last_batch = True
            self.data_pointer = 0
        return dataset, last_batch


    def __str__(self):
        return self.datafolder
#test batching
if __name__=="__main__":
    dataObj = DataObj("/home/nv3le/workspace/Doping/PySpacerSolver/MEDIA/backward_encoded_split_on_relu.smt2_240220_23_54_17/ind_gen_files", train_size = 0.8, batch_size = 1024)
    train_set = set(dataObj.train_dps)
    test_set = set(dataObj.test_dps)
    intersection = train_set.intersection(test_set)
    print("INTERSECTION:", intersection)
    assert(len(train_set.intersection(test_set)) == 0)
    train, last_batch = dataObj.next_batch(dataObj.train_dps, "train")
