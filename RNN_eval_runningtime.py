import subprocess
import glob
import time
from RNN_eval import get_lustre_variants, get_model_path, get_db_conn
import sys
from enum import Enum
import argparse
from pathlib import Path
import os
import traceback
import json
TIMELIMIT = 930
DEFAULT_MAX_LEVEL = 4294967295

class SpacerResult(Enum):
    SAT = 1
    UNSAT = 2
    UNKNOWN = 3
    ERROR = 4
    VARIANT_NOT_EXIST = 5
    TIMEOUT = 6


def run_50052(port):
    cmd = 'python /home/nle/workspace/Doping/X_grpc_server.py -F -p {}'.format(port).split()
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return p


def run_model_server(exp_folder, model_path, port):
    cmd = 'python /home/nle/workspace/Doping/RNN_grpc_server.py -S {} -M {} -I {} -p {}'.format(exp_folder,
                                                                                                model_path,
                                                                                                os.path.join(exp_folder, "ind_gen_files"),
                                                                                                port).split()
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return p


def run_z3(exp_smt2, port, max_level, ver):
    class TimedOutCP:
        def __init__(self, stdout, stderr):
            self.stdout = stdout.decode('ascii')
            self.stderr = stderr.decode('ascii')

    if max_level < DEFAULT_MAX_LEVEL:
        timelimit = TIMELIMIT*3
    else:
        timelimit = TIMELIMIT
    cmd = ['/home/nle/opt/z3grpc/build/z3',
           'fp.spacer.dump_benchmarks=true',
           'fp.spacer.dump_threshold=99999',
           'fp.spacer.use_expansion=false',
           'fp.spacer.arith.solver=6',
           'fp.print_statistics=true',
           'fp.spacer.use_h_inductive_generalizer={}'.format(str(ver)),
           'fp.spacer.use_inductive_generalizer=false',
           'fp.spacer.grpc_host_port=localhost:{}'.format(str(port)),
           'fp.validate=true',
           '-v:1',
           '-T:{}'.format(timelimit),
           'fp.spacer.max_level={}'.format(max_level),
           exp_smt2
           ]
    print(cmd)
    try:
        cp = subprocess.run(cmd, timeout = TIMELIMIT*4, capture_output=True, text = True)
        return cp
    except subprocess.TimeoutExpired as e:
        return TimedOutCP(e.stdout, e.stderr)
def parse_stderr(stderr):
    def get_val(v):
        if v.endswith(")"):
            v = v[:-1]
        if "." in v:
            return float(v)
        else:
            return int(v)

    results = {
        "total_time":930,
        "total_time_inside":930,
        "ind_gen_time":0,
        "ind_gen_total": 930,
        "ind_gen_outside": 0,
        "n_request": -1,
        "n_response": -1,
        "n_correct":-1,
        "decisions": -1,
        "time.pool_solver.smt.total": 930,
        "depth":1,
        "enter_level":0,
        "n_lemmas":2000, "indgen_fail": 6000}
    try:
        if isinstance(stderr, str):
            if not os.path.exists(stderr):
                return results

            with open(stderr, "r") as f:
                raw = f.readlines()
        else:
            raw = stderr
        for l in raw:
            if l.startswith("Entering level"):
                v = l.strip().split()[-1]
                results["enter_level"] = get_val(v)
            if l.startswith("total_requests"):
                k,v = l.strip().split(":")
                results["n_request"] = get_val(v)
            elif "time.pool_solver.smt.total " in l:
                k,v = l.strip().split()
                results["time.pool_solver.smt.total"] = get_val(v)
            elif "dirty_requests" in l:
                k,v = l.strip().split(":")
                results["n_response"] = get_val(v)
            elif ":SPACER-max-depth " in l:
                k,v = l.strip().split()
                results["depth"] = get_val(v)
            elif ":SPACER-num-lemmas" in l:
                k,v = l.strip().split()
                results["n_lemmas"] = get_val(v)
            elif "unsuccessful_answers" in l:
                k,v = l.strip().split(":")
                results["n_correct"] = get_val(v)
            elif ":decisions" in l:
                k,v = l.strip().split()
                results["decisions"] = get_val(v)
            elif "time.spacer.solve  " in l:
                k,v = l.strip().split()
                results["total_time"] = get_val(v)
            elif "time.spacer.solve.reach.gen.bool_ind   " in l:
                k,v = l.strip().split()
                results["ind_gen_total"] = get_val(v)
            elif "time.spacer.solve.reach.gen.bool_ind.outside" in l:
                k,v = l.strip().split()
                results["ind_gen_outside"] = get_val(v)
            elif ":bool-inductive-gen-failures" in l:
                k,v = l.strip().split()
                results["indgen_fail"] = get_val(v)
            results["ind_gen_time"] = results["ind_gen_total"] - results["ind_gen_outside"]
            results["total_time_inside"] = results["total_time"] - results["ind_gen_outside"]
            
    except:
        traceback.print_exc()
        return results
    return results

def parse_stdout(stdout):
    results = {"res": None}
    try:
        if isinstance(stdout, str):
            if not os.path.exists(stdout):
                results["res"] = SpacerResult.VARIANT_NOT_EXIST
                return results

            with open(stdout, "r") as f:
                raw = f.readlines()
        else:
            raw = stdout
        if len(raw)==0:
            results["res"] = SpacerResult.ERROR
            return results
        else:
            res = raw[-1].strip()
            if res == "sat":
                results["res"] = SpacerResult.SAT
            elif res == "unsat":
                results["res"] = SpacerResult.UNSAT
            elif res == "unknown":
                results["res"] = SpacerResult.UNKNOWN
            elif res == "timeout":
                results["res"] = SpacerResult.TIMEOUT
    except:
        results["res"] = SpacerResult.ERROR

    results["res"] = str(results["res"])
    return results
#  :time.spacer.solve                                   62.21
#  :time.spacer.solve.propagate                         4.26
#  :time.spacer.solve.reach                             57.94
#  :time.spacer.solve.reach.children                    0.43
#  :time.spacer.solve.reach.gen.bool_ind                54.48
#  :time.spacer.solve.reach.gen.bool_ind.outside_spacer 48.00)
# dirty_requests:81
# unsuccessful_answers:17

def parse_result(var_path, cp: subprocess.CompletedProcess):
    res = {"variant": var_path}
    res["stderr"] = parse_stderr(cp.stderr.strip().split("\n"))
    res["stdout"] = parse_stdout(cp.stdout.strip().split("\n"))
    print(res)
    return res

def spot_check(exp_folder, max_level, args):
    variant = str(exp_folder.parts[-1])
    print("spot checking {}".format(variant))
    print("querrying db...")
    db = get_db_conn()
    c= db.cursor()
    try:
        c.execute('''SELECT * FROM Dopey.RunningTime WHERE variant = %s''', (variant,))
    except:
        print(c.statement)

    rows = c.fetchall()
    assert(len(rows)==1)
    row = rows[0]
    print("Prev entry in DB")
    print(row)
    model = row[1]
    seed = row[0]

    model_path = '/home/nle/workspace/Doping_run_benchmark/lustre_all/{}/models/{}'.format(seed, model)

    input_file_path = os.path.join(exp_folder, "input_file.smt2")
    print("Model:", model_path)
    print("Max level:", max_level)
    print("Input file path:", input_file_path)
    if args.spacer:
        proc = run_50052(port = 40042)
    elif args.ropey:
        proc = run_model_server(exp_folder, model_path, port = 40042)
    time.sleep(5)
    if max_level == -1:
        pz3 = run_z3(input_file_path, port = 40042, max_level = DEFAULT_MAX_LEVEL, ver = args.ver)
    else:
        pz3 = run_z3(input_file_path, port = 40042, max_level = max_level, ver = args.ver)
    z3r = parse_result("spotcheck", pz3)
    print(pz3.stderr.strip())
    print(pz3.stdout.strip())
    proc.kill()


def eval_running_time_variants(exp_folder, variants, model_path, max_level, args):
    p50052 = run_50052(port = 50000 + int(args.port))
    p_model = run_model_server(exp_folder, model_path, port = 60000 + int(args.port))
    time.sleep(5)
    db = get_db_conn()
    c = db.cursor()

    for v in variants:
        variant_str = str(Path(v).parts[-2:]) if "variant" in v else str(Path(v).parts[-1])
        if max_level == -1:
            """
            if args.max_level = -1, we are running it up to the bound reached by vanilla Spacer.
            We will only do so if previously rnn is timedout or unknown
            """
            print("evaluating {}".format(v))
            try:
                c.execute('''
                SELECT * FROM Dopey.RunningTime
                WHERE
                variant = %s and model = %s
                ''', (variant_str,os.path.basename(model_path)))
            except:
                print("error in querrying. skip")
                continue
            row = c.fetchall()[0]

            prev_original_res = json.loads(row[3])
            prev_rnn_res  = json.loads(row[4])
            if prev_rnn_res["stdout"]["res"] not in ['SpacerResult.TIMEOUT', 'SpacerResult.UNKNOWN']:
                print("Is not an unsolved instance")
                continue
            # if prev_rnn_res["stderr"]["enter_level"] == prev_original_res["stderr"]["enter_level"]:
            #     print("Already went to same depth")
            #     continue
            if row[0] == row[2]:
                print("seed is variant. Not interesting")
                continue
            prev_original_depth = prev_original_res["stderr"]["enter_level"]
            print("prev max lvl:", prev_original_depth)
            max_level = prev_original_depth

            z3r = prev_original_res
        else:
            pz3 = run_z3(os.path.join(v, "input_file.smt2"), port = 50000 + int(args.port), max_level = DEFAULT_MAX_LEVEL)
            z3r = parse_result(v,pz3)
            max_level = args.max_level

        prnn = run_z3(os.path.join(v, "input_file.smt2"), port = 60000 + int(args.port), max_level = max_level)
        rnnr = parse_result(v, prnn)
        try:
            c.execute('''
                    REPLACE INTO Dopey.RunningTime
                    (seed, model, variant,
                    original_res, rnn_res,
                    ind_gen_time, total_time, total_time_inside, ind_gen_total, ind_gen_outside, ent_depth,
                    rnn_ind_gen_time, rnn_total_time, rnn_total_time_inside, rnn_ind_gen_total, rnn_ind_gen_outside, rnn_ent_depth,
                    QuickDropVer)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

            ''', (str(exp_folder.parts[-1]),
                os.path.basename(model_path),
                variant_str,
                json.dumps(z3r), json.dumps(rnnr),
                z3r["stderr"]["ind_gen_time"], z3r["stderr"]["total_time"], z3r["stderr"]["total_time_inside"], z3r["stderr"]["ind_gen_total"], z3r["stderr"]["ind_gen_outside"], z3r["stderr"]["enter_level"],
                  rnnr["stderr"]["ind_gen_time"], rnnr["stderr"]["total_time"], rnnr["stderr"]["total_time_inside"], rnnr["stderr"]["ind_gen_total"], rnnr["stderr"]["ind_gen_outside"], rnnr["stderr"]["enter_level"],
                  args.ver
                )
                    )
        except:
            print(c.statement)
            traceback.print_exc()


        db.commit()
    p50052.kill()

    p_model.kill()


if __name__=="__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument("--test_folder", help = "path to the test ind_gen_files folder", required = True)
    parser.add_argument("--port", type = int)
    parser.add_argument("--max_level", type=int, default = DEFAULT_MAX_LEVEL)
    parser.add_argument("--ver", type=int, default = 42)
    parser.add_argument("--spotcheck", action = 'store_true')
    parser.add_argument("--ropey", action = 'store_true')
    parser.add_argument("--spacer", action = 'store_true')
    args = parser.parse_args()

    spotcheck = args.spotcheck


    test_folder = Path(args.test_folder).absolute()
    exp_folder = test_folder.parent.absolute()
    max_level = args.max_level
    if spotcheck:
        spot_check(exp_folder, max_level, args)

    else:

        variants = get_lustre_variants(test_folder)

        model_path  = get_model_path(test_folder, n = 'ES', tag = "C*E_1*TrPer_1*embP_64*")
        if model_path is None:
            model_path  = get_model_path(test_folder, n = 1499, tag = "C*E_1*TrPer_1*embP_64*")
        print("Eval model\n", model_path)
        if model_path is None:
            exit(0)

        eval_running_time_variants(exp_folder, variants, model_path, max_level, args)
