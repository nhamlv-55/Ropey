import torch
# torch.set_default_tensor_type('torch.cuda.FloatTensor')
import torch.nn as nn
import torch.nn.functional as F
from Doping.pytorchtreelstm.treelstm import TreeLSTM
import Doping.pytorchtreelstm.treelstm.util as TLUtil
class Model(torch.nn.Module):
    '''
    This model use h_c as a feature in h_a and h_b.
    '''
    def __init__(self, vocab_size, sort_vocab_size, emb_dim = 10, const_emb_dim = 0, tree_dim = 10, use_const_emb = True, use_dot_product = True, dropout_rate = 0.5, device = torch.device('cuda')):
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
        #calculate the input size of tree_lstm based on flags
        self.treelstm_input_size = emb_dim * 2
        if self._use_const_emb:
            self.treelstm_input_size += self._const_emb_dim
        self.treelstm = TreeLSTM(self.treelstm_input_size, tree_dim).to(device)

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
        h_a_raw, c_a_raw, a_sz = self.forward_a_tree(lit_a, debug = debug)
        h_b_raw, c_b_raw, b_sz = self.forward_a_tree(lit_b, debug = debug)
        h_a = TLUtil.stack_last_h(h_a_raw, a_sz)
        h_b = TLUtil.stack_last_h(h_b_raw, b_sz)

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
        logits = self.fc2(self.dropout(F.relu(self.fc1(h))))
        if self.training:
            return logits.view(batch_size, -1), None
        else:
            return logits.view(batch_size, -1), {
                "h_a_raw": h_a_raw,
                "h_b_raw": h_b_raw,
            }

    def forward_a_tree(self, tree, context_features = None, debug = False):
        '''
        if context_features is not None, we are forwarding a L_a or L_b tree.
        if context_features is None, we are forwarding the C_tree.
        '''
        features = tree["features"].to(self.device)
        node_order = tree["node_order"].to(self.device)
        adjacency_list = tree["adjacency_list"].to(self.device)
        edge_order = tree["edge_order"].to(self.device)
        # print(features.shape)
        token_feat = features[:,0].long()
        sort_feat = features[:,1].long()

        # print("token_feat", token_feat.tolist())

        token_emb = self.emb(token_feat)
        sort_emb = self.sort_emb(sort_feat)
        # print(token_emb.shape)
        # print(const_emb.shape)
        if self._use_const_emb:
            const_emb = features[:, 2:2+self._emb_dim]*1.0
            const_emb = const_emb.to(self.device)
            if debug:
                print("token_emb", token_emb[0])
                print("sort_emb", sort_emb[0])
                print("const_emb", const_emb[0])
            features = torch.cat((token_emb, sort_emb, const_emb), dim = 1)
        else:
            features = torch.cat((token_emb, sort_emb), dim = 1)

        # features = token_emb
        h, c = self.treelstm(features, node_order, adjacency_list, edge_order)
        return h,c, tree["tree_sizes"] 
 
