#!/usr/bin/env bash

CPU=930
MEM=16384

filename=$(basename $1)
TARGET_DIR=$2
echo "filename" $1
echo "TARGET_DIR" $TARGET_DIR

cd $TARGET_DIR/$filename.folder/
echo $PWD
cp solving_z3_trace .z3-trace
python /home/nle/workspace/Doping/PySpacerSolver/generate_ind_gen_files.py -input . >/dev/null
PYTHONPATH=~/opt/z3squashed/build/python/:~/workspace/:~/opt/pysmt/ python3 /home/nle/workspace/Doping/PySpacerSolver/spacer_solver.py -input ind_gen_files/ -S ./ -gen_dataset -limit 100000 -skip-indgen 
