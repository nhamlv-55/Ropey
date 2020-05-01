import torch
from model import Model
from eval import *
from Doping.utils.Dataset import DataObj
import argparse
from flask import Flask, request
from flask_cors import CORS
from flask import render_template
import json
import glob
import os
import html
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

torch.no_grad()
parser = argparse.ArgumentParser()
"""
If matrix-path is provided, we are visualizing the X matrix
"""
parser.add_argument('--model-path', help='path to the .pt file')
parser.add_argument('--matrix-path', help='path to the X.json, L.json files')
parser.add_argument('--port', type= int, default=8080, help='port')
args = parser.parse_args()

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
        data = []
        for X in Xs:
            print(X)
            with open(X, "r") as f:
                X_data = json.load(f)
                X_data = X_data["X"]
                data.append(X_data)
        L_size = len(data[-1])
        with open(os.path.join(args.matrix_path, "L.json"), "r") as f:
            L = json.load(f)
        id2L = {}
        for k in L:
            idx = L[k]
            id2L[idx] = html.escape(k)
        json_vis_data = {"Xs": data, "L_size": L_size, "no_of_X": len(data), "L": id2L}
        return render_template('matrix_vis.html', context=json.dumps(json_vis_data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
