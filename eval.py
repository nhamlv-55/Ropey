import torch
from model import Model
from Doping.utils.Dataset import DataObj
import argparse
torch.no_grad()
parser = argparse.ArgumentParser()
parser.add_argument('--model-path', help='path to the .pt file')
args = parser.parse_args()

if __name__=="__main__":
    model_path = args.model_path

    checkpoint = torch.load(model_path)
    model_metadata = checkpoint['metadata']
    dataset_metadata = checkpoint['dataset']
    print(model_metadata)
    model = Model(dataset_metadata['vocab_size'],
                dataset_metadata['sort_size'],
                emb_dim = model_metadata['emb_dim'],
                tree_dim = model_metadata['tree_dim'],
                out_dim = 2,
                use_c = model_metadata['use_c'],
                use_const_emb = model_metadata['use_const_emb']).eval()

    dataObj = DataObj(datafolder = dataset_metadata['datafolder'],
                    max_size = dataset_metadata['max_size'],
                    shuffle = dataset_metadata['shuffle'],
                    train_size = dataset_metadata['train_size'],
                    batch_size = 1) # batchsize = 1 for visualization

    test, last_batch = dataObj.next_batch(dataObj.test_dps, "test")
    print(test)
    output = model(test["C_batch"], test["L_a_batch"], test["L_b_batch"])
    print(output)
