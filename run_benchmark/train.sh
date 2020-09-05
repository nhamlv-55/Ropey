#!/usr/bin/env bash

CPU=930
MEM=16384

echo "Start training for $1"
if grep -Fxq "$1" finished_training
then
    echo "$1 was trained to completion"
else
    # code if not found
    filename=$(basename $1)
    cd all_dataset/$filename.folder/
    cp solving_z3_trace .z3-trace


    PROJECT=/home/nv3le/workspace/Doping
    python3 $PROJECT/X_train.py --json_config_file $PROJECT/exp_config_pos.json 1>>X_train_stdout_pos 2>>X_train_stderr_pos
    python3 $PROJECT/X_train.py --json_config_file $PROJECT/exp_config_neg.json 1>>X_train_stdout_neg 2>>X_train_stderr_neg
fi

