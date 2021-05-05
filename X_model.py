import torch
import torch.nn as nn
import torch.nn.functional as F
from Doping.pytorchtreelstm.treelstm import TreeLSTM
import Doping.pytorchtreelstm.treelstm.util as TLUtil
from Doping.LemmaEncoder import LemmaEncoder
import Doping.utils.utils as Du

class Model(torch.nn.Module):
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
                 use_const_emb = True,
                 use_dot_product = True,
                 dropout_rate = 0.5,
                 device = torch.device('cuda'),
                 log_level = 'INFO'):
        super().__init__()
        print("VOCAB SIZE:", vocab_size)
        print("SORT SIZE", sort_vocab_size)
        print("USE CONSTANT EMB", use_const_emb)
        self.device = device
        self._emb_dim = emb_dim
        self._const_emb_dim = const_emb_dim
        self._tree_dim = tree_dim
        self._use_const_emb = use_const_emb
        self._use_dot_product = use_dot_product
        self._dropout_rate = dropout_rate
        self.emb = nn.Embedding(vocab_size*2, emb_dim ).to(self.device) #*2 to handle out of vocab cases
        self.sort_emb = nn.Embedding(sort_vocab_size*2, emb_dim ).to(self.device)
        self.dropout = nn.Dropout(p=self._dropout_rate)

        self.log = Du.create_logger(log_level, __name__)
        self.lemma_encoder = LemmaEncoder(vocab_size,
                                          sort_vocab_size,
                                          emb_dim,
                                          const_emb_dim,
                                          pos_emb_dim,
                                          tree_dim,
                                          use_const_emb,
                                          use_dot_product,
                                          dropout_rate,
                                          device,
                                          log_level = 'INFO')
        #calculate the size of the last layer before FNN
        self.next_to_last_size = tree_dim * 2
        if self._use_dot_product:
            self.next_to_last_size+=1

        self.fc1 = nn.Linear(self.next_to_last_size, tree_dim).to(self.device)
        self.fc2 = nn.Linear(tree_dim, 2).to(self.device)
        self.softmax = nn.Softmax(dim = 1)
    def metadata(self):
        return {"emb_dim": self._emb_dim,
                "const_emb_dim": self._const_emb_dim,
                "tree_dim": self._tree_dim,
                "use_const_emb": self._use_const_emb,
                "use_dot_product": self._use_dot_product,
                "dropout_rate": self._dropout_rate,
                "model": "new_model"
        }

    def forward(self, lit_a, lit_b, debug = False):
        #if use context, need to compute context features first
        h_a = self.lemma_encoder(lit_a, debug = debug)
        h_b = self.lemma_encoder(lit_b, debug = debug)
        assert(h_a.shape[0] == h_b.shape[0])
        batch_size = h_a.shape[0]

        #compute the dot product here
        if self._use_dot_product:
            dotp = torch.diag(torch.matmul(h_a, torch.t(h_b)))
            dotp = dotp.view(batch_size, 1, -1)

        h_a = h_a.view(batch_size, 1, -1)
        h_b = h_b.view(batch_size, 1, -1)

        h = torch.cat((h_a, h_b), dim = -1)
        if self._use_dot_product:
            h = torch.cat((h, dotp), dim = -1)
        h = h.squeeze()
        self.log.debug((h, h.size()))
        self.log.debug((self.fc1(h), self.fc1(h).size()))
        logits = self.fc2(self.dropout(F.relu(self.fc1(h))))

        return logits.view(batch_size, -1), None
