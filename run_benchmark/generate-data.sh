#!/usr/bin/env bash

CPU=930
MEM=16384

echo $1
filename=$(basename $1)
cd all_dataset/$filename.folder/
cp solving_z3_trace .z3-trace
python /home/nv3le/workspace/Doping/PySpacerSolver/generate_ind_gen_files.py -input . >/dev/null
PYTHONPATH=~/opt/z3squashed/build/python/:~/workspace/:~/opt/pysmt/ python3 /home/nv3le/workspace/Doping/PySpacerSolver/spacer_solver.py -input ind_gen_files/ -S ./ -gen_dataset -limit 100000 -skip-indgen 
# /home/nv3le/opt/z3grpc/build/z3 fp.spacer.dump_benchmarks=true fp.spacer.dump_threshold=99999 fp.spacer.use_expansion=false fp.spacer.arith.solver=6 fp.print_statistics=true fp.spacer.use_h_inductive_generalizer=42 fp.spacer.use_inductive_generalizer=false fp.spacer.grpc_host_port="localhost:50052" fp.validate=true -tr:spacer.ind_gen -T:$CPU -memory:$MEM input_file.smt2 1>stdout 2>stderr
# cp .z3-trace solving_z3_trace
# time $PROJECT/bin/z3-deep-space-static -st -v:1 fp.xform.slice=true fp.xform.inline_linear=true fp.xform.inline_eager=true fp.xform.tail_simplifier_pve=false fp.engine=spacer fp.print_statistics=true fp.spacer.elim_aux=$ELIM_AUX fp.spacer.reach_dnf=true fp.spacer.iuc=$IUC fp.spacer.iuc.arith=$IUC_ARITH fp.validate=true fp.spacer.ground_pobs=true fp.spacer.mbqi=false fp.spacer.iuc.print_farkas_stats=$IUC_FARKAS_STATS fp.spacer.iuc.old_hyp_reducer=$IUC_OLD_HYPREDUCE fp.spacer.ctp=true fp.spacer.native_mbp=$MBP -T:$CPU -memory:$MEM $1 

