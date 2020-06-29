import torch
from X_model import Model
from Doping.utils.X_Dataset import DataObj
import argparse

def setup_model(model_path):
    checkpoint = torch.load(model_path)
    model_metadata = checkpoint['metadata']
    dataset_metadata = checkpoint['dataset']
    print("Epoch", checkpoint["epoch"])

    model = Model(dataset_metadata['vocab_size'],
                  dataset_metadata['sort_size'],
                  emb_dim = 30, #30 is the max emb_dim possible, due to the legacy dataset
                  tree_dim = 100,
                  use_const_emb = model_metadata['use_const_emb'],
                  use_dot_product = model_metadata['use_dot_product'],
                  device = torch.device('cuda')).eval()

    model.load_state_dict(checkpoint["model_state_dict"])

    return model

if __name__=="__main__":
    torch.no_grad()
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', help='path to the .pt file')
    args = parser.parse_args()

    model_path = args.model_path
    model = setup_model(model_path)
    # run(model, dataObj, model_metadata)
