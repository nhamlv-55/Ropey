import torch
# torch.set_default_tensor_type('torch.cuda.FloatTensor')
import torch.nn as nn
import torch.nn.functional as F
from Doping.pytorchtreelstm.treelstm import TreeLSTM
import Doping.pytorchtreelstm.treelstm.util as TLUtil
import logging

class RNNModel(nn.Module):
    def __init__(self,
                 vocab_size,
                 sort_vocab_size,
                 emb_dim,
                 const_emb_dim,
                 tree_dim,
                 use_const_emb,
                 use_dot_product,
                 dropout_rate=0.5,
                 hidden_dim=64, 
                 output_dim = 2, 
                 n_layers = 1, 
                 bidirectional = True, 
                 pad_idx = None,
                 log_level = logging.DEBUG,
                 device = torch.device('cuda')):

        super().__init__()
        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_level)
        

        self.lemma_encoder = LemmaEncoder(vocab_size,
                                        sort_vocab_size,
                                        emb_dim,
                                        const_emb_dim,
                                        tree_dim,
                                        use_const_emb,
                                        use_dot_product,
                                        dropout_rate,
                                        device,
                                        self.log)

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
        self.log.debug(predictions, predictions.size())
        return predictions


class LemmaEncoder(torch.nn.Module):
    '''
    This model use h_c as a feature in h_a and h_b.
    '''
    def __init__(self, vocab_size, sort_vocab_size, emb_dim = 10, const_emb_dim = 0, tree_dim = 10, use_const_emb = True, use_dot_product = True, dropout_rate = 0.5, device = torch.device('cuda'), logger = None):
        super().__init__()

        if logger is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = logger

        self.log.debug("VOCAB SIZE:", vocab_size)
        self.log.debug("SORT SIZE", sort_vocab_size)
        self.log.debug("USE CONSTANT EMB", use_const_emb)
        self.device = device

        self._emb_dim = emb_dim
        self._const_emb_dim = const_emb_dim
        self._tree_dim = tree_dim
        self._use_const_emb = use_const_emb
        self._use_dot_product = use_dot_product
        self._dropout_rate = dropout_rate

        self._use_token_emb = True


        self.emb = nn.Embedding(vocab_size, emb_dim ).to(self.device) 
        self.sort_emb = nn.Embedding(sort_vocab_size, emb_dim ).to(self.device)
        self.dropout = nn.Dropout(p=self._dropout_rate)
        #calculate the input size of tree_lstm based on flags
        self.treelstm_input_size = emb_dim * 2
        if self._use_const_emb:
            self.treelstm_input_size += self._const_emb_dim
        self.treelstm = TreeLSTM(self.treelstm_input_size, tree_dim).to(device)

        #calculate the size of the last layer before FNN
        self.next_to_last_size = tree_dim * 2
        if self._use_dot_product:
            self.next_to_last_size+=1

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
                "tree_dim": self._tree_dim,
                "use_const_emb": self._use_const_emb,
                "use_dot_product": self._use_dot_product,
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

        # self.log.debug("token_feat", token_feat.tolist())
        if self._use_token_emb:
            token_emb = self.emb(token_feat)
        else:
            token_emb = torch.zeros([token_feat.shape[0], self._emb_dim], requires_grad = False).to(self.device)
        sort_emb = self.sort_emb(sort_feat)
        # self.log.debug(token_emb.shape)
        # self.log.debug(const_emb.shape)
        if self._use_const_emb:
            const_emb = features[:, 2:2+self._emb_dim]*1.0
            const_emb = const_emb.to(self.device)
            if debug:
                self.log.debug("token_emb", token_emb[0])
                self.log.debug("sort_emb", sort_emb[0])
                self.log.debug("const_emb", const_emb[0])
            features = torch.cat((token_emb, sort_emb, const_emb), dim = 1)
        else:
            const_emb = torch.zeros([token_feat.shape[0], self._const_emb_dim], requires_grad = False).to(self.device)
            features = torch.cat((token_emb, sort_emb, const_emb), dim = 1)

        # features = token_emb
        h, c = self.treelstm(features, node_order, adjacency_list, edge_order)


        self.log.debug(tree["tree_sizes"])
        h_root = TLUtil.stack_last_h(h, tree["tree_sizes"])

        return h_root
 
