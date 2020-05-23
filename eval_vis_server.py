import torch
from model import Model
from eval import *
from Doping.utils.Dataset import DataObj
from Doping.utils.utils import calculate_P

import argparse
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask import render_template
import json
import glob
import os
import html
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
CORS(app)

torch.no_grad()
parser = argparse.ArgumentParser()
"""
If matrix-path is provided, we are visualizing the X matrix
"""
parser.add_argument('--model-path', help='path to the .pt file')
parser.add_argument('--matrix-path', help='path to the X.json, L.json files')
parser.add_argument('--dataset-path', help='path to the folder containing multiple matrix path')
parser.add_argument('--port', type= int, default=8080, help='port')
parser.add_argument('--limit', type= int, default=50, help='visualize from t_0 to t_limit')
args = parser.parse_args()

def plot(folder):
    image_name = "XPM.svg"
    #immediately return if the image is previously built
    if os.path.isfile(os.path.join(folder, image_name)):
        return os.path.join(folder, image_name)


    try:
        with open(os.path.join(folder, "L.json"), "r") as f:
            L = json.load(f)
        with open(os.path.join(folder, "L_freq.json"), "r") as f:
            L_freq = json.load(f)

        with open(os.path.join(folder, "X00000.json"), "r") as f:
            last_X = json.load(f)["X"]
    except Exception as e:
        return "error in reading either L.json, L_freq.json, or X0***.json"

    last_P = calculate_P(last_X, L, L_freq)

    

    fig, (ax0, ax1, ax2) = plt.subplots(1, 3)
    im = ax0.imshow(np.asarray(last_X), interpolation = None)
    im = ax1.imshow(np.asarray(last_P), interpolation = None)
    im = ax2.imshow(np.asarray(last_X).astype(bool), interpolation = None)
    plt.savefig(os.path.join(folder, image_name), dpi=1000, bbox_inches='tight')
    fig.clf()
    return os.path.join(folder, image_name)

def detailed_plot(folder):
    try:
        with open(os.path.join(folder, "L.json"), "r") as f:
            L = json.load(f)
        with open(os.path.join(folder, "L_freq.json"), "r") as f:
            L_freq = json.load(f)

        with open(os.path.join(folder, "X00000.json"), "r") as f:
            last_X = json.load(f)["X"]
    except Exception as e:
        return "error in reading either L.json, L_freq.json, or X0***.json"

    last_P = calculate_P(last_X, L, L_freq).tolist()

    id2L = {}
    for k in L:
        idx = L[k]
        id2L[idx] = html.escape(k)
    json_vis_data = {"Xs": [last_X], "Ps": [last_P], "L_size": len(L), "no_of_X": 1, "L": id2L}
    return json_vis_data

@app.route('/static/<path:path>')
def send_img(path):
    return send_from_directory('', path)
if args.model_path is not None:
    model, dataObj, model_metadata = setup_model(args.model_path)
    @app.route('/vis/<h_index>', methods=['GET'])
    def handle_vis(h_index):
        json_vis_data = run(model, dataObj, model_metadata)
        return render_template('vis.html', context=json.dumps(json_vis_data), h_index = h_index)

if args.matrix_path is not None:
    @app.route('/vis', methods=['GET'])
    def handle_vis():
        Xs = glob.glob(args.matrix_path+"/X00*.json")
        Xs = sorted(Xs)
        Ps = glob.glob(args.matrix_path+"/P00*.json")
        Ps = sorted(Ps)
        #collect X data
        Xs_data = []
        limit = args.limit
        limit = min(len(Xs), limit)
        for X in Xs[:limit]:
            print(X)
            with open(X, "r") as f:
                X_data = json.load(f)
                X_data = X_data["X"]
                Xs_data.append(X_data)
        L_size = len(Xs_data[-1])

        #collect P data
        Ps_data = []
        for P in Ps[:limit]:
            print(P)
            with open(P, "r") as f:
                P_data = json.load(f)
                P_data = P_data["P"]
                Ps_data.append(P_data)

        with open(os.path.join(args.matrix_path, "L.json"), "r") as f:
            L = json.load(f)
        id2L = {}
        for k in L:
            idx = L[k]
            id2L[idx] = html.escape(k)

        assert(len(Xs_data) == len(Ps_data))
        
        json_vis_data = {"Xs": Xs_data, "Ps": Ps_data, "L_size": L_size, "no_of_X": len(Xs_data), "L": id2L}
        return render_template('matrix_vis.html', context=json.dumps(json_vis_data))

if args.dataset_path is not None:
    @app.route('/vis', methods=['GET'])
    def handle_vis():
        datapaths = glob.glob(args.dataset_path+"/*/ind_gen_files")
        datapaths = sorted(datapaths)
        json_vis_data = {}
        for dp in datapaths[:args.limit]:
            print(dp)
            json_vis_data[dp] = plot(dp)
       
        return render_template('dataset_vis.html', context=json.dumps(json_vis_data))
    @app.route('/detailed_vis/<ind_gen_path>', methods=['GET'])
    def handle_detailed_vis(ind_gen_path):
        print(ind_gen_path)
        ind_gen_path = ind_gen_path.replace("___", "/")
        json_vis_data = detailed_plot(ind_gen_path)
        return render_template('matrix_vis.html', context=json.dumps(json_vis_data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port )
