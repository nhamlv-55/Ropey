import glob
import os
import argparse
import pandas as pd
from pandas import DataFrame
import json
def parse_stderr(lines):
    metrics = {}
    for l in lines:
        l = l.strip()
        if l.startswith(":bool-inductive"):
            k, v = l.strip().split()
            metrics[k] = v
    return metrics

def parse_res_path(res_path):
    results = {}
    stderrs = glob.glob(res_path + "/*/*/*/stderr")
    for serr in stderrs:
        try:
            exp_path = os.path.dirname(serr)
            exp_name = exp_path[-17:]
            sout_path = os.path.join(exp_path, "stdout")

            with open(sout_path, "r") as f:
                res = f.readlines()[0].strip()
            with open(serr, "r") as f:
                lines = f.readlines()
                results[exp_name] = parse_stderr(lines)
            results[exp_name]["res"] = res
        except Exception as e:
            print("Error in parsing {}".format(serr))
    return DataFrame.from_dict(results, orient = 'index')
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-O', '--ori_res_path', help='path to the original results folder')
    parser.add_argument('-H', '--heu_res_path', help='path to the heuristic results folder')
    args = parser.parse_args()

    ori_res_path = args.ori_res_path
    heu_res_path = args.heu_res_path
   
    ori_res = parse_res_path(ori_res_path)
    heu_res = parse_res_path(heu_res_path)

    # print(json.dumps(ori_res, indent = 2))
    # print(json.dumps(heu_res, indent = 2))

    final = pd.concat([ori_res, heu_res], axis = 1)


    print(final)
   
