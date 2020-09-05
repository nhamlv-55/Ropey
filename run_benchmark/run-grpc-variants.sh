#!/usr/bin/env bash

CPU=930
MEM=16384

WORKDIR="/home/nv3le/workspace/Doping"

X_GRPC="$WORKDIR/X_grpc_server.py"

DATADIR="$WORKDIR/run_benchmark/all_dataset"

N_MODEL_PATTERN="TrNeg_True"
P_MODEL_PATTERN="TrNeg_False"

AUX_PATTERN="embD_10_treeD_32"

echo "basefile $1"

filename=$(basename $1)
port=6${filename:8:4}
echo "PORT = $port"
folder=$(dirname $1)

#find the latest N and P
P_MODEL=$(ls -t $DATADIR/$filename.folder/models/*$P_MODEL_PATTERN*$AUX_PATTERN*Epoch2999.pt | head -1)
N_MODEL=$(ls -t $DATADIR/$filename.folder/models/*$N_MODEL_PATTERN*$AUX_PATTERN*Epoch2999.pt | head -1)
echo "P_model = $P_MODEL"
echo "N_model = $N_MODEL"

#start X_grpc server
screen -d -m python3 $X_GRPC -S "$DATADIR/$filename.folder" \
	-I "$DATADIR/$filename.folder/ind_gen_files" \
	-P $P_MODEL \
	-N $N_MODEL \
	-p $port

sleep 10

for i in 0 1 2 3 4 5 6 7 8 9
do
   variant_folder="$DATADIR/$filename.folder/variant_$i"
   cd $variant_folder
   pwd
   /home/nv3le/opt/z3grpc/build/z3 fp.spacer.dump_benchmarks=true fp.spacer.dump_threshold=99999 fp.spacer.use_expansion=false fp.spacer.arith.solver=6 fp.print_statistics=true fp.spacer.use_h_inductive_generalizer=42 fp.spacer.use_inductive_generalizer=false fp.validate=true fp.spacer.grpc_host_port="localhost:$port" -T:$CPU -memory:$MEM input_file.smt2 1>stdout_grpc 2>stderr_grpc
done
pkill -f $filename.folder
