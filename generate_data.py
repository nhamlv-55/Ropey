import os
import argparse
import subprocess
import glob
import shutil
import time
import stat
# fp.spacer.dump_benchmarks=true -tr:spacer.ind_gen fp.spacer.use_expansion=false
z3_args = ['fp.spacer.max_level=20',
           'fp.spacer.dump_benchmarks=true',
           'fp.spacer.dump_threshold=99999',
           '-tr:spacer.ind_gen',
           'fp.spacer.use_expansion=false',
           'fp.spacer.arith.solver=6',
           # 'fp.spacer.trace_file=spacer.log',
           'fp.print_statistics=true' ,
           '-v:1'
           ]

cwd = os.getcwd()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--z3', help='path to the z3 binary')
    parser.add_argument('--input', help='path to the folder containing original smt2 problems')
    parser.add_argument('--output', help='path to the output folder')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    args = parser.parse_args()

    z3_path = args.z3
    input_folder = args.input
    output_folder = args.output
    logging = args.logLevel
    smt2_queries = glob.glob(input_folder+"/*.smt2")
    
    for q_file in smt2_queries:
        print(q_file)
        q_folder = "%s.folder"%q_file
        q_folder_path = os.path.join(output_folder, q_folder)
        if not os.path.exists(q_folder_path):
            os.makedirs(q_folder_path)
        shutil.copyfile(q_file, os.path.join(q_folder_path, 'input_file.smt2'))
        z3_run_command = []
        z3_run_command.append(z3_path)
        z3_run_command.extend(z3_args)
        z3_run_command.append('input_file.smt2')
        z3_run_command.append("1>stdout 2>stderr")
        z3_run_command = " ".join(z3_run_command)

        gen_ind_gen_command = ["python"]
        gen_ind_gen_command.append(os.path.join(cwd, "PySpacerSolver", "generate_ind_gen_files.py"))
        gen_ind_gen_command.append("-input .")
        if logging!='DEBUG':
            gen_ind_gen_command.append(">/dev/null")
        gen_ind_gen_command = " ".join(gen_ind_gen_command)

        spacer_solver_command = ["PYTHONPATH=~/opt/z3squashed/build/python/:~/workspace/:~/opt/pysmt/"]
        spacer_solver_command.append("python3")
        spacer_solver_command.append(os.path.join(cwd, "PySpacerSolver", "spacer_solver.py"))
        spacer_solver_command.append("-input ind_gen_files/")
        spacer_solver_command.append("-gen_dataset")
        spacer_solver_command.append("-skip-indgen")
        if logging!='DEBUG':
            spacer_solver_command.append(">/dev/null")
        spacer_solver_command = " ".join(spacer_solver_command)

        move_z3_trace = "cp .z3-trace solving_z3_trace"
        with open(os.path.join(q_folder_path, 'run_1.sh'), 'w') as f:
            f.write(z3_run_command)
            f.write("\n")
            f.write(move_z3_trace)
        with open(os.path.join(q_folder_path, 'run_2.sh'), 'w') as f:
            f.write(gen_ind_gen_command)
        with open(os.path.join(q_folder_path, 'run_3.sh'), 'w') as f:
            f.write(spacer_solver_command)

        with open(os.path.join(q_folder_path, 'run.sh'), 'w') as f:
            f.write("#! /usr/bin/bash\n")
            f.write(z3_run_command)
            f.write("\n")
            f.write(move_z3_trace)
            f.write("\n")
            f.write(gen_ind_gen_command)
            f.write("\n")
            f.write(spacer_solver_command)
            f.write("\n")
if __name__=="__main__":
    main()

