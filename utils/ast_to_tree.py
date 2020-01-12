import z3
import json

class Vocab:
    def __init__(self):
        self.id2w = {}
        self.w2id = {}
        self.size = 0

        #add constant
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


class Node:
    def __init__(self):
        self._token = ""
        self._token_id = -1
        self._children = list()
        self._sort = None
        self._num_child = 0
        self._node_idx = -1

    def keys(self):
        return ["children", "index", "features"]

    def __getitem__(self, key):
        # print("K:",key)
        if key=="children": return self._children
        elif key =="index": return self._node_idx
        elif key =="features": return self._token_id

    def __setitem__(self, key, value):
        if key=="children": return self.set_children(value)
        elif key =="index": return self.set_node_idx(value)


    def set_token(self, ast_node, vocab):
        if z3.is_rational_value(ast_node):
            self._token = "<NUMBER>"
            self._token_id = vocab.add_token(self._token)
        else:
            self._token = ast_node.decl().name()
            self._token_id = vocab.add_token(self._token)
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


    def to_json(self):
        if self._num_child==0:
            return {"token": self._token, "token_id": self._token_id, "sort": self._sort}
        else:
            return {"token": self._token, "token_id": self._token_id, "sort": self._sort, "children": [child.to_json() for child in self._children]}
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


