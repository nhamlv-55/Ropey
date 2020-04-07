import torch
from model import Model
from Doping.utils.Dataset import DataObj
import argparse

def setup_model(model_path):
    checkpoint = torch.load(model_path)
    model_metadata = checkpoint['metadata']
    dataset_metadata = checkpoint['dataset']

    model = Model(dataset_metadata['vocab_size'],
                dataset_metadata['sort_size'],
                emb_dim = model_metadata['emb_dim'],
                tree_dim = model_metadata['tree_dim'],
                out_dim = 2,
                use_c = model_metadata['use_c'],
                use_const_emb = model_metadata['use_const_emb']).eval()

    # datafolder = '1_tree_to_test_adj_list/'
    dataObj = DataObj(datafolder = dataset_metadata['datafolder'],
    # dataObj = DataObj(datafolder = datafolder,
                    max_size = dataset_metadata['max_size'],
                    shuffle = dataset_metadata['shuffle'],
                    train_size = dataset_metadata['train_size'],
                    batch_size = 1) # batchsize = 1 for visualization
    print("--------------------------")
    return model, dataObj, model_metadata

def run(model, dataObj, model_metadata):
    test, last_batch = dataObj.next_batch(dataObj.test_dps, "test")
    print(test)
    L_a_tree = test["L_a_batch"]
    L_b_tree = test["L_b_batch"]
    output = model(test["C_batch"], test["L_a_batch"], test["L_b_batch"])

    json_vis_data = {}
    json_vis_data["filename"] = test["filenames"]
    json_vis_data["node_a"] = list(range(L_a_tree['tree_sizes'][0]))
    json_vis_data["adj_list_a"] = L_a_tree["adjacency_list"].tolist()

    json_vis_data["node_b"] = list(range(L_b_tree['tree_sizes'][0]))
    json_vis_data["adj_list_b"] = L_b_tree["adjacency_list"].tolist()

    json_vis_data["h_a_raw"] = output[1]["h_a_raw"].tolist()
    json_vis_data["h_a_min"] = torch.min(output[1]["h_a_raw"], dim = 0)[0].tolist()
    json_vis_data["h_a_max"] = torch.max(output[1]["h_a_raw"], dim = 0)[0].tolist()

    json_vis_data["h_b_raw"] = output[1]["h_b_raw"].tolist()
    json_vis_data["h_b_min"] = torch.min(output[1]["h_b_raw"], dim = 0)[0].tolist()
    json_vis_data["h_b_max"] = torch.max(output[1]["h_b_raw"], dim = 0)[0].tolist()

    json_vis_data["vocab"] = dataObj.vocab
    json_vis_data["feature_a"] = L_a_tree["features"].tolist()
    json_vis_data["feature_b"] = L_b_tree["features"].tolist()
    json_vis_data["metadata"] = model_metadata
    return json_vis_data


if __name__=="__main__":
    torch.no_grad()
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', help='path to the .pt file')
    args = parser.parse_args()

    model_path = args.model_path
    model, dataObj, model_metadata = setup_model(model_path)
    run(model, dataObj, model_metadata)
