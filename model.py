import torch
import torch.nn as nn
import torch.nn.functional as F
from Doping.pytorchtreelstm.treelstm import TreeLSTM
class Model(torch.nn.Module):
    def __init__(self, vocab_size, emb_dim = 10, tree_dim = 10, out_dim = 3):
        super().__init__()
        self._emb_dim = emb_dim
        self._tree_dim = tree_dim
        self.emb = nn.Embedding(vocab_size, emb_dim)
        self.treelstm = TreeLSTM(emb_dim, tree_dim)
        self.fc1 = nn.Linear(tree_dim, int(tree_dim/2))
        self.fc2 = nn.Linear(int(tree_dim/2), out_dim)

    def forward(self, cube, lit_a, lit_b):
        h_c, c_c = self.forward_a_tree(cube)
        h_c = h_c[-1]
        h_a, c_a = self.forward_a_tree(lit_a)
        h_a = h_a[-1].view(self._tree_dim, 1)
        h_b, c_b = self.forward_a_tree(lit_b)
        h_b = h_b[-1].view(1, self._tree_dim)

        # print(h_a.shape, h_b.shape, h_c.shape)
        fuse_a_b = torch.matmul(h_a, h_b)
        # print(fuse_a_b.shape)
        h = torch.matmul(fuse_a_b, h_c)
        # print(h.shape)
        return F.relu(self.fc2(F.relu(self.fc1(h))))

    def forward_a_tree(self, tree):
        features = tree["features"]
        node_order = tree["node_order"]
        adjacency_list = tree["adjacency_list"]
        edge_order = tree["edge_order"]
        features = self.emb(features)
        h, c = self.treelstm(features, node_order, adjacency_list, edge_order)
        return h,c 
 
