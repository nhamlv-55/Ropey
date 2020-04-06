import torch
from model import Model
from eval import *
from Doping.utils.Dataset import DataObj
import argparse
from flask import Flask, request
from flask_cors import CORS
from flask import render_template
import json
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

torch.no_grad()
parser = argparse.ArgumentParser()
parser.add_argument('--model-path', help='path to the .pt file')
parser.add_argument('--port', type= int, default=8080, help='port')
args = parser.parse_args()

model, dataObj = setup_model(args.model_path)

@app.route('/vis')
def handle_vis():
    json_vis_data = run(model, dataObj)
    return render_template('vis.html', data=json.dumps(json_vis_data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
