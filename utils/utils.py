import z3
import json
import torch
from Doping.pytorchtreelstm.treelstm import calculate_evaluation_orders
# from Doping.PySpacerSolver.utils import *
import os
# class Vocab:
#     def __init__(self):
#         self.id2w = {}
#         self.w2id = {}
#         self.size = 0

#         self.id2s = {}
#         self.s2id = {}
#         self.sort_size = 0

#         self.id2const = {}
#         self.const2id = {}
#         self.const_size = 0

#         #add constant
#         self.add_token("<ROOT>")
#         self.add_token("<UNK>")

#         self.add_sort("<ROOT>")
#         self.add_sort("<UNK>")

#     def add_token(self, w):
#         '''add a token to vocab and return its id'''
#         if w in self.w2id:
#             return self.w2id[w]
#         else:
#             idx = self.size
#             self.w2id[w] = idx
#             self.id2w[idx] = w
#             self.size+=1
#             return self.w2id[w]

#     def add_sort(self, sort):
#         '''add a sort to vocab and return its id'''
#         if sort in self.s2id:
#             return self.s2id[sort]
#         else:
#             idx = self.sort_size
#             self.s2id[sort] = idx
#             self.id2s[idx] = sort
#             self.sort_size+=1
#             return self.s2id[sort]

#     def add_const(self, const):
#         '''add a const to vocab and return its id'''
#         if const in self.const2id:
#             return self.const2id[const]
#         else:
#             idx = self.const_size
#             self.const2id[const] = idx
#             self.id2const[idx] = const
#             self.const_size+=1
#             return self.const2id[const]

#     def dump(self):
#         print("ID2W:", self.id2w)
#         print("W2ID:", self.w2id)

#     def save(self, filename):
#         vocab = {"id2w": self.id2w, "w2id": self.w2id, "size": self.size, "id2s": self.id2s, "s2id": self.s2id, "sort_size": self.sort_size, "const2id": self.const2id, "id2const": self.id2const, "const_size": self.const_size}
#         with open(filename, "w") as f:
#             json.dump(vocab, f)
# class Node:
#     def __init__(self):
#         self._raw_expr = ""
#         self._token = ""
#         self._token_id = -1
#         self._sort_id = -1
#         self._children = list()
#         self._sort = None
#         self._num_child = 0
#         self._node_idx = -1

#     def keys(self):
#         return ["children", "index", "features"]

#     def __getitem__(self, key):
#         if key=="children": return self._children
#         elif key =="index": return self._node_idx
#         elif key =="features": return self.get_feat()
#         elif key =="token_id": return self._token_id
#     def __setitem__(self, key, value):
#         if key=="children": return self.set_children(value)
#         elif key =="index": return self.set_node_idx(value)


#     def set_token(self, ast_node, vocab):
#         if z3.is_rational_value(ast_node):
#             self._token = "<NUMBER>"
#             _ = vocab.add_const(str(ast_node))
#             self._token_id = vocab.add_token(self._token)
#             self._raw_expr = str(ast_node)
#         else:
#             self._token = ast_node.decl().name()
#             self._token_id = vocab.add_token(self._token)
#             self._raw_expr = str(ast_node)



#     def set_sort(self, ast_node, vocab):
#         if z3.is_const(ast_node):
#             if z3.is_bool(ast_node):
#                 sort = "<BOOL_VAR>"
#             elif ast_node == 0:
#                 sort = "<ZERO>"
#             elif z3.is_int(ast_node):
#                 if ast_node < 0:
#                     sort = "<NEG_INT>"
#                 else:
#                     sort = "<POS_INT>"
#             elif z3.is_rational_value(ast_node):
#                 fl = float(ast_node.numerator_as_long())/float(ast_node.denominator_as_long())
#                 if fl < 0:
#                     sort = "<NEG_RAT>"
#                 else:
#                     sort = "<POS_RAT>"
#             else:
#                 sort = "<VAR>"
#         elif ast_node.decl().name() == "and":
#             sort = "<AND>"
#         else:
#             sort = ast_node.sort().name()
#         self._sort = sort
#         self._sort_id = vocab.add_sort(self._sort)
#     def set_node_idx(self, idx):
#         self._node_idx = idx

#     def get_node_idx(self):
#         return self._node_idx

#     def token(self):
#         return self._token

#     def sort(self):
#         return self._sort

#     def set_children(self, children):
#         self._children = children
#         self._num_child = len(children)

#     def children(self):
#         return self._children

#     def set_as_root(self, vocab):
#         self._token = "<ROOT>"
#         self._token_id = vocab.add_token(self._token)
#         self._raw_expr = "<ROOT>"
#         self._sort = "<ROOT>"
#         self._sort_id = vocab.add_sort(self._sort)

#     def to_json(self):
#         if self._num_child==0:
#             return {"token": self._token, "token_id": self._token_id, "sort": self._sort, "sort_id": self._sort_id, "children": [], "expr": self._raw_expr, "features": self.get_feat()}
#         else:
#             return {"token": self._token, "token_id": self._token_id, "sort": self._sort, "sort_id": self._sort_id, "children": [child.to_json() for child in self._children], "expr": self._raw_expr, "features": self.get_feat()}
#     def __str__(self):
#         return json.dumps(self.to_json(), indent = 2)

#     def rewrite(self):
#         if self._num_child==0:
#             return "%s|%s"%(self._token, self._sort)
#         else:
#             childs = [child.rewrite() for child in self._children]
#             childs = " ".join(childs)
#             return "(%s (%s))"%(self._token, childs)
            

#     def get_feat(self):
#         return [self._token_id, self._sort_id]

# def ast_to_node(ast_node, vocab):
#     node = Node()
#     node.set_token(ast_node, vocab)
#     node.set_sort(ast_node, vocab)
#     if ast_node.num_args == 0:
#         return node
#     else:
#         node.set_children([ast_to_node(child, vocab) for child in ast_node.children()])
#         return node

# def rootify(ast_node, vocab):
#     '''
#     attach the tree to a dummy node called ROOT to make sure everything is a tree (even a single node)
#     '''
#     root_node = Node()
#     root_node.set_as_root(vocab)
#     root_node.set_children([ast_node])
#     return root_node

# def ast_to_tree(ast_node, vocab):
#     return rootify(ast_to_node(ast_node, vocab), vocab)

# def _label_node_index(node, n=0):
#     node['index'] = n
#     for child in node['children']:
#         n += 1
#         _label_node_index(child, n)


# def _gather_node_attributes(node, key):
#     if key in node.keys():
#         features = [node[key]]

#     for child in node['children']:
#         features.extend(_gather_node_attributes(child, key))
#     return features


# def _gather_adjacency_list(node):
#     adjacency_list = []
#     for child in node['children']:
#         adjacency_list.append([node['index'], child['index']])
#         adjacency_list.extend(_gather_adjacency_list(child))

#     return adjacency_list


# def convert_tree_to_tensors(tree, device=torch.device('cuda')):
#     # Label each node with its walk order to match nodes to feature tensor indexes
#     # This modifies the original tree as a side effect
#     _label_node_index(tree)
#     features = _gather_node_attributes(tree, 'features')
#     adjacency_list = _gather_adjacency_list(tree)

#     # print("LEN FEATURES", len(features))
#     # print("ADJ LIST", adjacency_list)
#     node_order, edge_order = calculate_evaluation_orders(adjacency_list, len(features))

#     return {
#         'features': torch.tensor(features, device=device, dtype=torch.int64),
#         'node_order': torch.tensor(node_order, device=device, dtype=torch.int64),
#         'adjacency_list': torch.tensor(adjacency_list, device=device, dtype=torch.int64),
#         'edge_order': torch.tensor(edge_order, device=device, dtype=torch.int64),
#     }

# class Dataset:
#     def __init__(self, html_vis_page = None):
#         self.vocab = Vocab()
#         self.dataset = {}
#         if html_vis_page is not None:
#             self.html_vis_page = HtmlVisPage(html_vis_page)
#         else:
#             self.html_vis_page = None

#     def print2html(self, s, color = "black"):
#         print(s)
#         if self.html_vis_page is not None:
#             self.html_vis_page.write(html_colored(s, color))


#     def normalize(self, ast):
#         return z3.simplify(ast, arith_ineq_lhs = True, sort_sums = True)

#     def normalize_cube(self, cube):
#         new_cube = []
#         for l in cube:
#             new_cube.append(self.normalize(l))
#         return new_cube

#     def check_lit_conflict(self, cube, inducted_cube, filename):
#         '''
#         Check if exists 2 lits that are the same after tokenization, but one is red and one is blue
#         '''
#         self.print2html("Checking for lit conflict")
        
#         #a set contain all the lits that stays after ind_gen
#         conflict = False
#         blue_trees = set()
#         red_trees = set()
#         for lit in cube:
#             if lit in inducted_cube:
#                 blue_trees.add(ast_to_tree(lit, self.vocab).rewrite())
#             else:
#                 red_trees.add(ast_to_tree(lit, self.vocab).rewrite())

#         for lit in cube:
#             lit_tree = ast_to_tree(lit, self.vocab).rewrite()
#             if lit in inducted_cube and lit_tree not in red_trees:
#                 self.print2html("%s =====> %s"%(lit, lit_tree), "blue")
#             elif lit in inducted_cube and lit_tree in red_trees:
#                 conflict = True
#                 self.print2html("%s =====> %s"%(lit, lit_tree), "purple")
#             elif lit not in inducted_cube and lit_tree in blue_trees:
#                 conflict = True
#                 self.print2html("%s =====> %s"%(lit, lit_tree), "purple")
#             elif lit not in inducted_cube and lit_tree not in blue_trees:
#                 self.print2html("%s =====> %s"%(lit, lit_tree), "red")

#         self.print2html("----------------------------")
#         return conflict

#     def add_dp(self, cube, inducted_cube, filename):
#         if len(cube)<=1:
#             return
#         #Normalize before doing anything
#         self.print2html("normalize the cube")

#         self.print2html("raw cube")
#         visualize(cube, inducted_cube, self.html_vis_page)

#         self.print2html("normalized cube")
#         cube = self.normalize_cube(cube)
#         inducted_cube = self.normalize_cube(inducted_cube)
#         visualize(cube, inducted_cube, self.html_vis_page)

#         #Check for conflict
#         if self.check_lit_conflict(cube, inducted_cube, filename):
#             self.print2html("There is a self-conflict. Drop this cube")
#             return



#         last_collision_file = None

#         for i in range(len(cube)):

#             for j in range(i+1, len(cube)):
#                 '''4 possible labels: both lits are dropped 0, only one is dropped 1, non is dropped 2'''
#                 if cube[i] in inducted_cube and cube[j] in inducted_cube:
#                     label = 0
#                 elif cube[i] not in inducted_cube and cube[j] not in inducted_cube:
#                     label = 0
#                 else:
#                     label = 1

#                 C_tree = ast_to_tree(z3.And(cube), self.vocab)
#                 L_a_tree = ast_to_tree(cube[i], self.vocab)
#                 L_b_tree = ast_to_tree(cube[j], self.vocab)

#                 dp_filename = filename+ "."+ str(i)+ "."+ str(j)+ ".dp.json"
#                 X = (C_tree.rewrite(), L_a_tree.rewrite(), L_b_tree.rewrite())
#                 datapoint = {"filename": filename, "cube": cube, "inducted_cube": inducted_cube, "label": label}

#                 if X in self.dataset and self.dataset[X]["label"]!=label:
#                     if last_collision_file is None:
#                         self.print2html("Exist a same datapoint with a different label")
#                         self.print2html("PREVIOUS ENTRY")
#                         self.print2html(self.dataset[X]["filename"])
#                         visualize(self.dataset[X]["cube"], self.dataset[X]["inducted_cube"], self.html_vis_page)
#                         self.print2html("THIS ENTRY")
#                         self.print2html(filename)
#                         visualize(cube, inducted_cube, self.html_vis_page)
#                         last_collision_file = self.dataset[X]["filename"]
#                 else:
#                     self.dataset[X] = datapoint
#                 with open(dp_filename, "w") as f:
#                     json.dump({"C_tree": C_tree.to_json(), "L_a_tree": L_a_tree.to_json(), "L_b_tree": L_b_tree.to_json(), "label": label}, f)

#     def save_vocab(self, folder):
#         print("SAVING VOCAB")
#         self.vocab.save(os.path.join(folder, "vocab.json"))

#     def dump_dataset(self, folder):
#         pass
#         print("DUMPING DATASET IN TOKEN FORMAT")
#         with open(os.path.join(folder, "ds_token_form.json"), "w") as f:
#             json.dump(self.dataset, f, indent = 2)

#     def dump_html(self):
#         if self.html_vis_page is not None:
#             self.html_vis_page.dump()
