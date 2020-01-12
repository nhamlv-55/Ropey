import torch
import torch.nn as nn
import z3
from Doping.pytorchtreelstm.treelstm import TreeLSTM, calculate_evaluation_orders

import Doping.utils.ast_to_tree as Du

def _label_node_index(node, n=0):
    print(n)
    node['index'] = n
    for child in node['children']:
        n += 1
        _label_node_index(child, n)


def _gather_node_attributes(node, key):
    if key in node.keys():
        features = [node[key]]
    elif key == "labels": #only for testing
        features = [[0]]

    counter = 0
    for child in node['children']:
        print(counter)
        counter+=1
        print(key)
        features.extend(_gather_node_attributes(child, key))
    return features


def _gather_adjacency_list(node):
    adjacency_list = []
    for child in node['children']:
        adjacency_list.append([node['index'], child['index']])
        adjacency_list.extend(_gather_adjacency_list(child))

    return adjacency_list


def convert_tree_to_tensors(tree, device=torch.device('cpu')):
    # Label each node with its walk order to match nodes to feature tensor indexes
    # This modifies the original tree as a side effect
    _label_node_index(tree)
    features = _gather_node_attributes(tree, 'features')
    labels = _gather_node_attributes(tree, 'labels')
    adjacency_list = _gather_adjacency_list(tree)

    node_order, edge_order = calculate_evaluation_orders(adjacency_list, len(features))

    return {
        'features': torch.tensor(features, device=device, dtype=torch.int64),
        'labels': torch.tensor(labels, device=device, dtype=torch.float32),
        'node_order': torch.tensor(node_order, device=device, dtype=torch.int64),
        'adjacency_list': torch.tensor(adjacency_list, device=device, dtype=torch.int64),
        'edge_order': torch.tensor(edge_order, device=device, dtype=torch.int64),
    }

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

    data = convert_tree_to_tensors(tree)
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
