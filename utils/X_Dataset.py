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
    def __init__(self, datafolder, name = "dataset", shuffle = True, max_size = -1, train_size = 0.67, threshold = 0.75):
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
        self.train_size = train_size
        self.shuffle = shuffle
        
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
                "threshold": self.threshold,
        }

    def get_vocab(self):
        vocab_file = os.path.join(self.datafolder, "vocab.json")
        with open(vocab_file, "r") as f:
            self.vocab = json.load(f)

    def _build_P(self, suffix):
        with open(os.path.join(self.datafolder, "X" + suffix), "r") as f:
            X = json.load(f)["X"]
        with open(os.path.join(self.datafolder, "L" + suffix ), "r") as f:
            L = json.load(f)
        with open(os.path.join(self.datafolder, "L_freq" + suffix ), "r") as f:
            L_freq = json.load(f)

        P = calculate_P(X, L, L_freq)
        return P


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

        X_mats = glob.glob(self.datafolder + "/X0*.json")
        X_mats = sorted(X_mats)

        
        train_index = int(len(X_mats)*self.train_size)
        X_train_filename = os.path.basename(X_mats[train_index])
        X_test_filename = os.path.basename(X_mats[-1])
        #expect X_train_filename to be X00***.json, then suffix would be 00***.json
        train_suffix = X_train_filename[1:]
        log.info("train_suffix:{}".format(train_suffix))
        test_suffix  = X_test_filename[1:]
        log.info("test_suffix:{}".format(test_suffix))

        self.train_P = self._build_P(train_suffix)
        self.test_P = self._build_P(test_suffix)


    def next_batch(self, P_matrix, batch_size, negative_sampling_rate):
        last_batch = False
        dataset = {}
        filenames = []
        L_a_trees = []
        L_b_trees = []
        labels = []
        log.debug("data_pointer:{}".format(self.data_pointer))
        log.debug(len(P_matrix))

        if negative_sampling_rate==-1:#if not using negative sampling
            for i in range(self.data_pointer, min(self.data_pointer + batch_size, len(P_matrix))):
                #at row_i
                for j in range(len(P_matrix[i])):
                    # print(self.lits[i])
                    L_a_trees.append(self.lits[i])
                    L_b_trees.append(self.lits[j])
                    labels.append(int(P_matrix[i][j]> self.threshold))
        else:#if using negative sampling
            pos_samples = []
            neg_samples = []
            for i in range(self.data_pointer, min(self.data_pointer + batch_size, len(P_matrix))):
                #at row_i
                for j in range(len(P_matrix[i])):
                    # print(self.lits[i])
                    if (P_matrix[i][j] > self.threshold):
                        pos_samples.append((i, j, 1))
                    else:
                        neg_samples.append((i, j, 0))

            n_neg_samples = len(pos_samples)*negative_sampling_rate
            neg_samples = random.sample(neg_samples, n_neg_samples)

            all_samples = pos_samples + neg_samples
            random.shuffle(all_samples)
            log.debug("Use negative sampling. Number of datapoints for this batch:{}".format(len(all_samples)))
            for (i,j,label) in all_samples:
                L_a_trees.append(self.lits[i])
                L_b_trees.append(self.lits[j])
                labels.append(int(label))


        dataset["size"] = len(L_a_trees)
        dataset["L_a_batch"] = batch_tree_input(L_a_trees)
        dataset["L_b_batch"] = batch_tree_input(L_b_trees)
        dataset["label_batch"] = torch.tensor(labels)
        dataset["filenames"] = filenames
        self.data_pointer+=batch_size
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
