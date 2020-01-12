import torch

from treelstm import TreeLSTM, calculate_evaluation_orders


def _label_node_index(node, n=0):
    node['index'] = n
    for child in node['children']:
        n += 1
        _label_node_index(child, n)


def _gather_node_attributes(node, key):
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

    features = _gather_node_attributes(tree, 'features')
    labels = _gather_node_attributes(tree, 'labels')
    adjacency_list = _gather_adjacency_list(tree)

    node_order, edge_order = calculate_evaluation_orders(adjacency_list, len(features))

    return {
        'features': torch.tensor(features, device=device, dtype=torch.float32),
        'labels': torch.tensor(labels, device=device, dtype=torch.float32),
        'node_order': torch.tensor(node_order, device=device, dtype=torch.int64),
        'adjacency_list': torch.tensor(adjacency_list, device=device, dtype=torch.int64),
        'edge_order': torch.tensor(edge_order, device=device, dtype=torch.int64),
    }


if __name__ == '__main__':
    # Toy example
    tree = {
        'features': [1, 0], 'labels': [1], 'children': [
            {'features': [0, 1], 'labels': [0], 'children': []},
            {'features': [0, 0], 'labels': [0], 'children': [
                {'features': [1, 1], 'labels': [0], 'children': []}
            ]},
        ],
    }

    data = convert_tree_to_tensors(tree)

    model = TreeLSTM(2, 1).train()

    loss_function = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters())

    for n in range(1000):
        optimizer.zero_grad()

        h, c = model(
            data['features'],
            data['node_order'],
            data['adjacency_list'],
            data['edge_order']
        )

        labels = data['labels']
        print(h.shape)
        print(labels.shape)
        loss = loss_function(h, labels)
        loss.backward()
        optimizer.step()

        # print(f'Iteration {n+1} Loss: {loss}')
    print(data)
