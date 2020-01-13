import z3
import json
import torch
from Doping.pytorchtreelstm.treelstm import calculate_evaluation_orders
class Vocab:
    def __init__(self):
        self.id2w = {}
        self.w2id = {}
        self.size = 0

        #add constant
        self.add_token("<ROOT>")
        self.add_token("<NUMBER>")
        self.add_token("<UNK>")
    
    def add_token(self, w):
        '''add a token to vocab and return its id'''
        if w in self.w2id:
            return self.w2id[w]
        else:
            idx = self.size
            self.w2id[w] = idx
            self.id2w[idx] = w
            self.size+=1
            return self.w2id[w]

    def dump(self):
        print("ID2W:", self.id2w)
        print("W2ID:", self.w2id)

    def save(self, filename):
        vocab = {"id2w": self.id2w, "w2id": self.w2id, "size": self.size}
        with open(filename, "w") as f:
            json.dump(vocab, f)
class Node:
    def __init__(self):
        self._raw_expr = ""
        self._token = ""
        self._token_id = -1
        self._children = list()
        self._sort = None
        self._num_child = 0
        self._node_idx = -1

    def keys(self):
        return ["children", "index", "features"]

    def __getitem__(self, key):
        if key=="children": return self._children
        elif key =="index": return self._node_idx
        elif key =="features": return self._token_id
        elif key =="token_id": return self._token_id
    def __setitem__(self, key, value):
        if key=="children": return self.set_children(value)
        elif key =="index": return self.set_node_idx(value)


    def set_token(self, ast_node, vocab):
        if z3.is_rational_value(ast_node):
            self._token = "<NUMBER>"
            self._token_id = vocab.add_token(self._token)
            self._raw_expr = str(ast_node)
        else:
            self._token = ast_node.decl().name()
            self._token_id = vocab.add_token(self._token)
            self._raw_expr = str(ast_node)



    def set_sort(self, ast_node):
        self._sort = ast_node.sort().name()

    def set_node_idx(self, idx):
        self._node_idx = idx

    def get_node_idx(self):
        return self._node_idx

    def token(self):
        return self._token

    def sort(self):
        return self._sort

    def set_children(self, children):
        self._children = children
        self._num_child = len(children)

    def children(self):
        return self._children

    def set_as_root(self, vocab):
        self._token = "<ROOT>"
        self._token_id = vocab.add_token(self._token)
        self._raw_expr = "<ROOT>"

    def to_json(self):
        if self._num_child==0:
            return {"token": self._token, "token_id": self._token_id, "sort": self._sort, "children": [], "expr": self._raw_expr}
        else:
            return {"token": self._token, "token_id": self._token_id, "sort": self._sort, "children": [child.to_json() for child in self._children], "expr": self._raw_expr}
    def __str__(self):
        return json.dumps(self.to_json(), indent = 2)

def ast_to_node(ast_node, vocab):
    node = Node()
    node.set_token(ast_node, vocab)
    node.set_sort(ast_node)
    if ast_node.num_args == 0:
        return node
    else:
        node.set_children([ast_to_node(child, vocab) for child in ast_node.children()])
        return node

def rootify(ast_node, vocab):
    '''
    attach the tree to a dummy node called ROOT to make sure everything is a tree (even a single node)
    '''
    root_node = Node()
    root_node.set_as_root(vocab)
    root_node.set_children([ast_node])
    return root_node

def ast_to_tree(ast_node, vocab):
    return rootify(ast_to_node(ast_node, vocab), vocab)

def _label_node_index(node, n=0):
    node['index'] = n
    for child in node['children']:
        n += 1
        _label_node_index(child, n)


def _gather_node_attributes(node, key):
    if key in node.keys():
        features = [node[key]]

    for child in node['children']:
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
    features = _gather_node_attributes(tree, 'token_id')
    adjacency_list = _gather_adjacency_list(tree)

    # print("LEN FEATURES", len(features))
    # print("ADJ LIST", adjacency_list)
    node_order, edge_order = calculate_evaluation_orders(adjacency_list, len(features))

    return {
        'features': torch.tensor(features, device=device, dtype=torch.int64),
        'node_order': torch.tensor(node_order, device=device, dtype=torch.int64),
        'adjacency_list': torch.tensor(adjacency_list, device=device, dtype=torch.int64),
        'edge_order': torch.tensor(edge_order, device=device, dtype=torch.int64),
    }

