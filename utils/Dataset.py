import Doping.PySpacerSolver.utils as DPu
from Doping.pytorchtreelstm.treelstm import batch_tree_input
import glob
import json
import torch
from sklearn.model_selection import train_test_split
import os
import random
class DataObj:
    def __init__(self, datafolder, name = "dataset", shuffle = True, max_size = -1, batch_size = -1, train_size = 0.67):
        '''
        datafolder: path to the /ind_gen_files folder
        name: name of the dataset
        shuffle: whether to shuffle the dataset. If this is set to False, the dataset will be ordered by the order in which the datapoints appear
        max_size: how many datapoints to use (test+ train). To test the performance after some certain spacer's checkpoints.
        batch_size: batch_size for training
        train_size: how much of the dataset is used for training
        '''
        self.datafolder = datafolder
        self.all_dps = []
        self._size = 0
        self._max_size = max_size
        self._total_dps = 10000
        self.train = {}
        self.test = {}
        self.vocab = {}
        self.all_dps = []
        self.train_dps = []
        self.test_dps = []
        self.data_pointer = 0
        self.batch_size = batch_size
        self.train_size = train_size
        self.shuffle = shuffle
        self.build_dataset()
        self.get_vocab()

    def metadata(self):
        return {"datafolder": self.datafolder,
                "size": self._size,
                "max_size": self._max_size,
                "train_size": self.train_size,
                "vocab_size": self.vocab['size'],
                "sort_size": self.vocab['sort_size'],
                "shuffle": self.shuffle,
                "batch_size": self.batch_size
        }

    def get_vocab(self):
        vocab_file = os.path.join(self.datafolder, "vocab.json")
        with open(vocab_file, "r") as f:
            self.vocab = json.load(f)


    def build_dataset(self):
        self.datafolder = os.path.join(self.datafolder, "")
        self.all_dps = glob.glob(self.datafolder+"/*.dp.json")
        self.all_dps = sorted(self.all_dps)
        self._total_dps = min(len(self.all_dps), self._total_dps)
        self.all_dps = self.all_dps[:self._total_dps]
        self._size = len(self.all_dps)
        if self.shuffle:
            random.shuffle(self.all_dps)
        train_index = int(self._size*self.train_size)

        #only use up to max_size dps for the training set
        self.train_dps = []
        assert(self._max_size < train_index)
        #if max_size == -1, use all the dps
        if self._max_size == -1:
            for i in range(train_index):
                self.train_dps.append(self.all_dps[i])
        else:
            for i in range( train_index - self._max_size, train_index):
                self.train_dps.append(self.all_dps[i])
        self.test_dps = []
        for i in range(train_index, len(self.all_dps)):
            self.test_dps.append(self.all_dps[i])

        # assert(len(self.train_dps)+len(self.test_dps) == len(self.all_dps))

        self.train = self._dataset_from_dps(self.train_dps, "train")
        self.test = self._dataset_from_dps(self.test_dps, "test")

    def _dataset_from_dps(self, all_dps, name):
        dataset = {}
        C_trees = []
        L_a_trees = []
        L_b_trees = []
        labels = []
        for dp in all_dps:
            with open(dp, "r") as f:
                data  = json.load(f)
                C_trees.append(DPu.convert_tree_to_tensors(data["C_tree"]))
                L_a_trees.append(DPu.convert_tree_to_tensors(data["L_a_tree"]))
                L_b_trees.append(DPu.convert_tree_to_tensors(data["L_b_tree"]))
                labels.append(data["label"])

        dataset["name"] = name
        dataset["size"] = len(all_dps)
        dataset["C_batch"] = batch_tree_input(C_trees)
        dataset["L_a_batch"] = batch_tree_input(L_a_trees)
        dataset["L_b_batch"] = batch_tree_input(L_b_trees)
        dataset["label_batch"] = torch.tensor(labels)
        return dataset

    def next_batch(self, all_dps, name):
        last_batch = False
        dataset = {}
        filenames = []
        C_trees = []
        L_a_trees = []
        L_b_trees = []
        labels = []
        for dp in all_dps[self.data_pointer: min(self.data_pointer + self.batch_size, len(all_dps))]:
            with open(dp, "r") as f:
                data  = json.load(f)
                filenames.append(dp)
                C_trees.append(DPu.convert_tree_to_tensors(data["C_tree"]))
                L_a_trees.append(DPu.convert_tree_to_tensors(data["L_a_tree"]))
                L_b_trees.append(DPu.convert_tree_to_tensors(data["L_b_tree"]))
                labels.append(data["label"])

        dataset["name"] = name
        dataset["size"] = len(C_trees)
        dataset["C_batch"] = batch_tree_input(C_trees)
        dataset["L_a_batch"] = batch_tree_input(L_a_trees)
        dataset["L_b_batch"] = batch_tree_input(L_b_trees)
        dataset["label_batch"] = torch.tensor(labels)
        dataset["filenames"] = filenames
        self.data_pointer+=self.batch_size
        if self.data_pointer>len(all_dps):
            last_batch = True
            self.data_pointer = 0
        return dataset, last_batch


    def size(self):
        return self._size


#test batching
if __name__=="__main__":
    dataObj = DataObj("/home/nv3le/workspace/Doping/PySpacerSolver/MEDIA/backward_encoded_split_on_relu.smt2_240220_23_54_17/ind_gen_files", train_size = 0.8, batch_size = 1024)
    train_set = set(dataObj.train_dps)
    test_set = set(dataObj.test_dps)
    intersection = train_set.intersection(test_set)
    print("INTERSECTION:", intersection)
    assert(len(train_set.intersection(test_set)) == 0)
    train, last_batch = dataObj.next_batch(dataObj.train_dps, "train")
