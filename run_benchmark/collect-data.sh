#!/usr/bin/env bash

CPU=930
MEM=16384
# TARGET_DIR="all_dataset"
filename=$(basename $1)
TARGET_DIR=$2
echo "filename" $1
echo "TARGET_DIR" $TARGET_DIR
mkdir -p $TARGET_DIR/$filename.folder
cp $1 $TARGET_DIR/$filename.folder/input_file.smt2
cd $TARGET_DIR/$filename.folder/
/home/nle/opt/z3grpc/build/z3 fp.spacer.dump_benchmarks=true fp.spacer.dump_threshold=99999 fp.spacer.use_expansion=false fp.spacer.arith.solver=6 fp.print_statistics=true fp.spacer.use_h_inductive_generalizer=42 fp.spacer.use_inductive_generalizer=false fp.spacer.grpc_host_port="localhost:50052" fp.validate=true -tr:spacer.ind_gen -T:$CPU -memory:$MEM input_file.smt2 1>stdout 2>stderr
cp .z3-trace solving_z3_trace

