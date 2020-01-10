import z3
import json
class Node:
    def __init__(self):
        self._token = ""
        self._children = list()
        self._sort = None
        self._num_child = 0
    def set_token(self, ast_node):
        if z3.is_rational_value(ast_node):
            self._token = "<NUMBER>"
        else:
            self._token = ast_node.decl().name()

    def set_sort(self, ast_node):
        self._sort = ast_node.sort().name()

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
            return {"token": self._token, "sort": self._sort}
        else:
            return {"token": self._token, "sort": self._sort, "children": [child.to_json() for child in self._children]}
    def __str__(self):
        return json.dumps(self.to_json(), indent = 2)

def ast_to_node(ast_node):
    node = Node()
    node.set_token(ast_node)
    node.set_sort(ast_node)
    if ast_node.num_args == 0:
        return node
    else:
        node.set_children([ast_to_node(child) for child in ast_node.children()])
        return node


