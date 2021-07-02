import torch
# torch.set_default_tensor_type('torch.cuda.FloatTensor')
import torch.nn as nn
import torch.nn.functional as F
from Doping.pytorchtreelstm.treelstm import TreeLSTM
import Doping.pytorchtreelstm.treelstm.util as TLUtil
import Doping.utils.utils as Du
from Doping.LemmaEncoder import LemmaEncoder

import logging
class RNNModel(nn.Module):
    def __init__(self,
                 vocab_size,
                 sort_vocab_size,
                 emb_dim,
                 const_emb_dim,
                 pos_emb_dim,
                 tree_dim,
                 dropout_rate=0.5,
                 hidden_dim=64, 
                 output_dim = 2, 
                 n_layers = 1, 
                 bidirectional = True, 
                 pad_idx = None,
                 log_level = "DEBUG",
                 device = torch.device('cuda'),
                 use_var_emb = True):

        super().__init__()
       
        self.log = Du.create_logger(log_level, __name__)

        self.lemma_encoder = LemmaEncoder(vocab_size,
                                          sort_vocab_size,
                                          emb_dim,
                                          const_emb_dim,
                                          pos_emb_dim,
                                          tree_dim,
                                          dropout_rate,
                                          device,
                                          log_level,
                                          use_var_emb)

        self.lstm = nn.LSTM(tree_dim, 
                            hidden_dim, 
                            num_layers = n_layers, 
                            bidirectional = bidirectional,
                            dropout = dropout_rate if n_layers > 1 else 0,
                            batch_first = True).to(device)

        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim).to(device)

        self.dropout = nn.Dropout(dropout_rate).to(device)

    def metadata(self):
        return {"lemma_encoder": self.lemma_encoder.metadata() }

    def disable_token_emb(self):
        self.lemma_encoder.disable_token_emb()

    def enable_token_emb(self):
        self.lemma_encoder.enable_token_emb()

    def disable_constant_emb(self):
        self.lemma_encoder.disable_constant_emb()

    def enable_constant_emb(self):
        self.lemma_encoder.enable_constant_emb()

    def forward(self, cube):
        ##XXX: currently expect only a single cube, not a batch
        #text = [sent len, batch size]

        feat_h = self.lemma_encoder(cube).unsqueeze(0)
        self.log.debug(feat_h.size())

        #embedded = [sent len, batch size, emb dim]

        #pass embeddings into LSTM
        outputs, (hidden, cell) = self.lstm(feat_h)

        #outputs holds the backward and forward hidden states in the final layer
        #hidden and cell are the backward and forward hidden and cell states at the final time-step

        #output = [sent len, batch size, hid dim * n directions]
        #hidden/cell = [n layers * n directions, batch size, hid dim]

        #we use our outputs to make a prediction of what the tag should be
        predictions = self.fc(self.dropout(outputs)).squeeze()

        #predictions = [sent len, batch size, output dim]
        self.log.debug((predictions, predictions.size()))
        return predictions
