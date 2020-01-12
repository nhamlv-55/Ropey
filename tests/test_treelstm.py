import torch
import torch.nn as nn
import z3
from Doping.pytorchtreelstm.treelstm import TreeLSTM, calculate_evaluation_orders

import Doping.utils.utils as Du

class Model(torch.nn.Module):
    def __init__(self, vocab_size, emb_dim = 10, tree_dim = 1):
        super().__init__()
        self._emb_dim = emb_dim
        self.emb = nn.Embedding(vocab_size, emb_dim)
        self.treelstm = TreeLSTM(emb_dim, tree_dim)

    def forward(self, features, node_order, adjacency_list, edge_order):
        features = self.emb(features)
        h, c = self.treelstm(features, node_order, adjacency_list, edge_order)
        return h,c 
        


if __name__ == '__main__':

    x1, x2, x3 = z3.Reals('x1 x2 x3')
    x1_f = z3.Bool('x1_f')
    expr = z3.And((70/17*x1 + 2*x2)<10, x1_f, (x1>10))
    print(expr)
    vocab = Du.Vocab()
    tree = Du.ast_to_node(expr, vocab)
    print(tree)
    # Toy example
    # tree = {
    #     'features': [1, 0], 'labels': [1], 'children': [
    #         {'features': [0, 1], 'labels': [0], 'children': []},
    #         {'features': [0, 0], 'labels': [0], 'children': [
    #             {'features': [1, 1], 'labels': [0], 'children': []}
    #         ]},
    #     ],
    # }

    data = Du.convert_tree_to_tensors(tree)
    print(data)
    # model = TreeLSTM(100, 1).train()

    model = Model(vocab.size).train()
    loss_function = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters())

    for n in range(100):
        optimizer.zero_grad()

        h, c = model(
            data['features'],
            data['node_order'],
            data['adjacency_list'],
            data['edge_order']
        )

        labels = data['labels']
        loss = loss_function(h, labels)
        loss.backward()
        optimizer.step()

        print(f'Iteration {n+1} Loss: {loss}')
    print(data)
