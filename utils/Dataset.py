import Doping.utils.utils as Du
from Doping.pytorchtreelstm.treelstm import batch_tree_input
import glob
import json
import torch
class Dataset:
    def __init__(self, datafolder, name = "dataset"):
        self.datafolder = datafolder
        self._size = 0
        self.C_batch = None
        self.L_a_batch = None
        self.L_b_batch = None
        self.label_batch = None
        self.build_dataset()

    def build_dataset(self):
        all_dps = glob.glob(self.datafolder+"/*.dp.json")
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

        self._size = len(all_dps)
        self.C_batch = batch_tree_input(C_trees)
        self.L_a_batch = batch_tree_input(L_a_trees)
        self.L_b_batch = batch_tree_input(L_b_trees)
        self.label_batch = torch.tensor(labels)

    def size(self):
        return self._size
