import torch
import torch.nn as nn
import torch.nn.functional as F
from Doping.pytorchtreelstm.treelstm import TreeLSTM
import Doping.pytorchtreelstm.treelstm.util as TLUtil
import Doping.utils.utils as Du
import logging

import math
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=50000, device = torch.device('cuda')):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model).to(device)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)
    def forward(self, x):
        x = self.pe[x, :]
        return self.dropout(x)

class LemmaEncoder(torch.nn.Module):
    '''
    This model use h_c as a feature in h_a and h_b.
    '''
    def __init__(self,
                 vocab_size,
                 sort_vocab_size,
                 emb_dim = 10,
                 const_emb_dim = 0,
                 pos_emb_dim = 32,
                 tree_dim = 10,
                 dropout_rate = 0.5,
                 device = torch.device('cuda'),
                 log_level = 'INFO'):
        super().__init__()
        self.log = Du.create_logger(log_level, __name__)
        self.positional_encoding = PositionalEncoding(pos_emb_dim, device = device)

        self.device = device

        self._emb_dim = emb_dim
        self._const_emb_dim = const_emb_dim
        self._pos_emb_dim = pos_emb_dim
        self._tree_dim = tree_dim
        self._dropout_rate = dropout_rate

        self._use_const_emb = (const_emb_dim > 0)
        self._use_token_emb = True
        self._use_pos_emb = (pos_emb_dim > 0)

        self.emb = nn.Embedding(vocab_size, emb_dim ).to(self.device)
        self.sort_emb = nn.Embedding(sort_vocab_size, emb_dim ).to(self.device)
        self.dropout = nn.Dropout(p=self._dropout_rate)
        #calculate the input size of tree_lstm based on flags
        self.treelstm_input_size = emb_dim * 2
        if self._use_const_emb:
            self.treelstm_input_size += self._const_emb_dim
        if self._use_pos_emb:
            self.treelstm_input_size += self._pos_emb_dim


        self.log.info(("treelstm_input_size", self.treelstm_input_size, self._pos_emb_dim, self._const_emb_dim, self._emb_dim))
        self.log.debug(("VOCAB SIZE:", vocab_size))
        self.log.debug(("SORT SIZE", sort_vocab_size))
        self.log.debug(("USE CONSTANT EMB", self._use_const_emb))

        self.treelstm = TreeLSTM(self.treelstm_input_size, tree_dim).to(device)

    def disable_token_emb(self):
        if self._use_token_emb:
            print("Disable token embeddings...")
            self._use_token_emb = False

    def enable_token_emb(self):
        if not self._use_token_emb:
            print("Enable token embeddings...")
            self._use_token_emb = True

    def disable_constant_emb(self):
        if self._use_const_emb:
            print("Disable const embeddings...")
            self._use_const_emb = False

    def enable_constant_emb(self):
        if not self._use_const_emb:
            print("Enable const embeddings...")
            self._use_const_emb = True


    def metadata(self):
        return {"emb_dim": self._emb_dim,
                "const_emb_dim": self._const_emb_dim,
                "pos_emb_dim": self._pos_emb_dim,
                "tree_dim": self._tree_dim,
                "use_const_emb": self._use_const_emb,
                "dropout_rate": self._dropout_rate,
                "model": "new_model"
        }

    def forward(self, tree, context_features = None, debug = False):
        '''
        if context_features is not None, we are forwarding a L_a or L_b tree.
        if context_features is None, we are forwarding the C_tree.
        '''
        features = tree["features"].to(self.device)
        node_order = tree["node_order"].to(self.device)
        adjacency_list = tree["adjacency_list"].to(self.device)
        edge_order = tree["edge_order"].to(self.device)
        # self.log.debug(features.shape)
        token_feat = features[:,0].long()
        sort_feat = features[:,1].long()
        position_feat = features[:,2].long()

        fixed_feats = [token_feat, sort_feat, position_feat]


        # self.log.debug("token_feat", token_feat.tolist())
        if self._use_token_emb:
            token_emb = self.emb(token_feat)
        else:
            token_emb = torch.zeros([token_feat.shape[0], self._emb_dim], requires_grad = False).to(self.device)
        sort_emb = self.sort_emb(sort_feat)
        # self.log.debug(token_emb.shape)
        # self.log.debug(const_emb.shape)
        if self._use_const_emb:
            const_emb = features[:, len(fixed_feats):len(fixed_feats)+self._const_emb_dim]*1.0
            const_emb = const_emb.to(self.device)
            if debug:
                self.log.debug("token_emb", token_emb[0])
                self.log.debug("sort_emb", sort_emb[0])
                self.log.debug("const_emb", const_emb[0])
        else:
            const_emb = torch.zeros([token_feat.shape[0], self._const_emb_dim], requires_grad = False).to(self.device)

        pos_emb = self.positional_encoding(position_feat).squeeze()
        self.log.debug((pos_emb, pos_emb.size()))
        features = torch.cat((token_emb, sort_emb, const_emb, pos_emb), dim = 1)

        # features = token_emb
        h, c = self.treelstm(features, node_order, adjacency_list, edge_order)


        self.log.debug(tree["tree_sizes"])
        h_root = TLUtil.stack_last_h(h, tree["tree_sizes"])

        return h_root
 
