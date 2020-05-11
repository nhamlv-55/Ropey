import Doping.PySpacerSolver.utils as DPu
from Doping.pytorchtreelstm.treelstm import batch_tree_input
import glob
import json
import torch
from sklearn.model_selection import train_test_split
import os
import random
class DataObj:
    def __init__(self, datafolder, name = "dataset", shuffle = True, max_size = -1, batch_size = -1, train_size = 0.67, threshold = 0.75):
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
        self.lits = []
        self.vocab = {}
        self.train_dps = []
        self.test_dps = []
        self.data_pointer = 0
        self.batch_size = batch_size
        self.train_size = train_size
        self.shuffle = shuffle

        self.Ps = None
        self.train_P = None
        self.test_P = None
        self.threshold = threshold

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
                "batch_size": self.batch_size,
                "threshold": self.threshold
        }

    def get_vocab(self):
        vocab_file = os.path.join(self.datafolder, "vocab.json")
        with open(vocab_file, "r") as f:
            self.vocab = json.load(f)


    def build_dataset(self):
        self.datafolder = os.path.join(self.datafolder, "")
        self.lit_files = glob.glob(self.datafolder+"/lit_*.json")
        self.lit_files = sorted(self.lit_files)
        self._size = len(self.lit_files)
        self.lits = {}
        #pre convert all lit tree to tensors
        for lf in self.lit_files:
            with open(lf, "r") as f:
                lit = json.load(f)
                # print(lit)
                lit_index = lit["index"]
                assert(lit_index not in self.lits)
                lit_tree = DPu.convert_tree_to_tensors(lit["tree"])
                self.lits[lit_index] = lit_tree


        self.Ps = glob.glob(self.datafolder + "/P00*.json")
        self.Ps = sorted(self.Ps)
        self.test_P = self.Ps[-1]
        no_of_P = len(self.Ps)
        self.train_P = self.Ps[int(no_of_P*self.train_size)]
        with open(self.train_P, "r") as f:
            self.train_dps = json.load(f)["P"]

        self.test_P = self.Ps[-1]
        with open(self.test_P, "r") as f:
            self.test_dps = json.load(f)["P"]
        print("Training P:")
        for i in self.train_dps:
            print(["{0:0.2f}".format(j) for j in i])
        print("Testing P:", self.test_dps)
        for i in self.test_dps:
            print(["{0:0.2f}".format(j) for j in i])

        #only use up to max_size dps for the training set
        # self.train_dps = []
        # assert(self._max_size < self.training_P)
        # #if max_size == -1, use all the dps
        # if self._max_size == -1:
        #     for i in range(train_index):
        #         self.train_dps.append(self.all_dps[i])
        # else:
        #     for i in range( train_index - self._max_size, train_index):
        #         self.train_dps.append(self.all_dps[i])
        # self.test_dps = []
        # for i in range(train_index, len(self.all_dps)):
        #     self.test_dps.append(self.all_dps[i])


    def next_batch(self, P_matrix, name):
        last_batch = False
        dataset = {}
        filenames = []
        C_trees = []
        L_a_trees = []
        L_b_trees = []
        labels = []
        print("training from row {} to row {} of the matrix training_P".format(self.data_pointer, min(self.data_pointer + self.batch_size, len(P_matrix))))
        for i in range(self.data_pointer, min(self.data_pointer + self.batch_size, len(P_matrix))):
            #at row_i
            
            for j in range(len(P_matrix[i])):
                # print(self.lits[i])
                L_a_trees.append(self.lits[i])
                L_b_trees.append(self.lits[j])
                labels.append(int(P_matrix[i][j]> self.threshold))

        dataset["size"] = len(L_a_trees)
        dataset["L_a_batch"] = batch_tree_input(L_a_trees)
        dataset["L_b_batch"] = batch_tree_input(L_b_trees)
        dataset["label_batch"] = torch.tensor(labels)
        dataset["filenames"] = filenames
        self.data_pointer+=self.batch_size
        if self.data_pointer>len(P_matrix):
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
