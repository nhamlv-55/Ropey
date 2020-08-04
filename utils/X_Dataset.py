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
    def __init__(self, datafolder, name = "dataset", shuffle = True, max_size = -1, train_size = 0.67, threshold = 0.75, negative = False):
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

        self.negative = negative
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

    def build_P(self, filename):
        """
        expect file name to be positive_X_00001.json or negative_X_00001.json
        """
        tokens = filename.split("_")
        suffix = tokens[-1]

        if self.negative:
            with open(os.path.join(self.datafolder, filename), "r") as f:
                X = json.load(f)["X"]
            with open(os.path.join(self.datafolder, "negative_lits_map" + suffix ), "r") as f:
                L = json.load(f)
            with open(os.path.join(self.datafolder, "negative_lits_map" + suffix ), "r") as f:
                L = json.load(f)
            with open(os.path.join(self.datafolder, "P_negative_X_matrix_" + suffix ), "r") as f:
                print(f.name)
                P = json.load(f)["X"]

        else:
            with open(os.path.join(self.datafolder, filename), "r") as f:
                X = json.load(f)["X"]
            with open(os.path.join(self.datafolder, "positive_lits_map" + suffix ), "r") as f:
                L = json.load(f)
            with open(os.path.join(self.datafolder, "positive_lits_count" + suffix ), "r") as f:
                L_freq = json.load(f)

            P = calculate_P(X, L, L_freq)
        return P

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
        if self.negative:
            self.lit_files = glob.glob(self.datafolder+"/negative_lit_*.json")
        else:
            self.lit_files = glob.glob(self.datafolder+"/positive_lit_*.json")
        self.lit_files = sorted(self.lit_files)
        self.size = len(self.lit_files)
        #pre convert all lit tree to tensors
        for lf in self.lit_files:
            with open(lf, "r") as f:
                lit = json.load(f)
                # print(lit)
                lit_index = lit["index"]
                assert(lit_index not in self.id2lits_json)
                lit_tree = DPu.convert_tree_to_tensors(lit["tree"])
                self.id2lits_json[lit_index] = {"lit_tree": lit_tree, "filename": lf}

        #load lits_map
        if self.negative:
            lits_maps = glob.glob(self.datafolder + "/negative_lits_map*.json")
        else:
            lits_maps = glob.glob(self.datafolder + "/positive_lits_map*.json")

        lits_maps = sorted(lits_maps)
        lits_map_file = lits_maps[-1]
        with open(lits_map_file, "r") as f:
            self.lits_str2id = json.load(f)

        if self.negative:
            X_mats = glob.glob(self.datafolder + "/negative_X_*.json")
            X_mats = sorted(X_mats)
        else:
            print(self.datafolder)
            X_mats = glob.glob(self.datafolder + "/positive_X_*.json")
            X_mats = sorted(X_mats)
        
        train_index = int(len(X_mats)*self.train_size)-1
        X_train_filename = os.path.basename(X_mats[train_index])
        X_test_filename = os.path.basename(X_mats[-1])

        self.train_P = self.build_P(X_train_filename)
        self.test_P = self.build_P(X_test_filename)


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
                    # print(self.id2lits_json[i])
                    L_a_trees.append(self.id2lits_json[i]["lit_tree"])
                    L_b_trees.append(self.id2lits_json[j]["lit_tree"])
                    filenames.append((self.id2lits_json[i]["filename"], self.id2lits_json[j]["filename"]))
                    if self.threshold>0:
                        labels.append(int(P_matrix[i][j]> self.threshold))
                    else:
                        labels.append(int(P_matrix[i][j] <= self.threshold))
        else:#if using negative sampling
            pos_samples = []
            neg_samples = []
            for i in range(self.data_pointer, min(self.data_pointer + batch_size, len(P_matrix))):
                #at row_i
                for j in range(len(P_matrix[i])):
                    if self.threshold>0:
                        if (P_matrix[i][j] > self.threshold):
                            pos_samples.append((i, j, 1))
                        else:
                            neg_samples.append((i, j, 0))
                    else:
                        if (P_matrix[i][j] <= self.threshold):
                            pos_samples.append((i, j, 1))
                        else:
                            neg_samples.append((i, j, 0))

            if self.threshold > 0 and len(pos_samples)>0:
                n_neg_samples = len(pos_samples)*negative_sampling_rate
                neg_samples = random.sample(neg_samples, n_neg_samples)

            all_samples = pos_samples + neg_samples
            random.shuffle(all_samples)
            log.debug("Use negative sampling. Number of datapoints for this batch:{}".format(len(all_samples)))
            for (i,j,label) in all_samples:
                L_a_trees.append(self.id2lits_json[i]["lit_tree"])
                L_b_trees.append(self.id2lits_json[j]["lit_tree"])
                filenames.append((self.id2lits_json[i]["filename"], self.id2lits_json[j]["filename"]))
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
