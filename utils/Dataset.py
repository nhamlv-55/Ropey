import Doping.utils.utils as Du
from Doping.pytorchtreelstm.treelstm import batch_tree_input
import glob
import json
import torch
from sklearn.model_selection import train_test_split
import os
import random
class DataObj:
    def __init__(self, datafolder, name = "dataset", shuffle = True):
        self.datafolder = datafolder
        self.all_dps = []
        self._size = 0
        self.train = {}
        self.test = {}
        self.vocab = {}
        self.shuffle = shuffle(x)
        self.build_dataset()
        self.get_vocab()

    def get_vocab(self):
        vocab_file = os.path.join(self.datafolder, "vocab.json")
        with open(vocab_file, "r") as f:
            self.vocab = json.load(f)


    def build_dataset(self, train_size = 0.67):
        self.datafolder = os.path.join(self.datafolder, "")
        all_dps = glob.glob(self.datafolder+"/*.dp.json")
        all_dps = sorted(all_dps)
        if self.shuffle:
            random.shuffle(all_dps)
        train_index = int(len(all_dps)*train_size)

        train_dps = all_dps[:train_index]
        test_dps = all_dps[train_index:]

        assert(len(train_dps)+len(test_dps) == len(all_dps))

        self.train = self._dataset_from_dps(train_dps, "train")
        self.test = self._dataset_from_dps(test_dps, "test")

    def _dataset_from_dps(self, all_dps, name):
        dataset = {}
        C_trees = []
        L_a_trees = []
        L_b_trees = []
        labels = []
        for dp in all_dps:
            with open(dp, "r") as f:
                data  = json.load(f)
                C_trees.append(Du.convert_tree_to_tensors(data["C_tree"]))
                L_a_trees.append(Du.convert_tree_to_tensors(data["L_a_tree"]))
                L_b_trees.append(Du.convert_tree_to_tensors(data["L_b_tree"]))
                labels.append(data["label"])

        dataset["name"] = name
        dataset["size"] = len(all_dps)
        dataset["C_batch"] = batch_tree_input(C_trees)
        dataset["L_a_batch"] = batch_tree_input(L_a_trees)
        dataset["L_b_batch"] = batch_tree_input(L_b_trees)
        dataset["label_batch"] = torch.tensor(labels)
        return dataset

    def size(self):
        return self._size

