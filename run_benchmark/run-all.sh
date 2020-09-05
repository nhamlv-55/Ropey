#!/bin/bash

#SBATCH --time=00:30:00
#SBATCH --account=def-arie
#SBATCH --cpus-per-task=32
#SBATCH --job-name=quic
#SBATCH --mem-per-cpu=8G

DATE=$(date +%d_%m_%Y-t%H-%M-%S)
PROJECT=/home/nv3le/workspace/Doping
SCRATCH=/home/nv3le/workspace/Doping

OUT=$SCRATCH/origin_out/lra.deep-space.lilla.$DATE

echo "Creating directory: $OUT"
mkdir -p $OUT

PROG1=$PROJECT/run_benchmark/collect-data.sh
PROG2=$PROJECT/run_benchmark/generate-data.sh
PROG3=$PROJECT/run_benchmark/train.sh
PROG4=$PROJECT/run_benchmark/run-grpc-variants.sh

PARALLEL=/usr/bin/parallel

# time $PARALLEL -j 8 --dryrun --ungroup --results $OUT/{/} $PROG :::: $PROJECT/run_benchmark/lra-files
# $PARALLEL -j 32 --results $OUT/{/} $PROG1 {} :::: $PROJECT/run_benchmark/lra-files
# $PARALLEL -j 32 --results $OUT/{/} $PROG2 {} :::: $PROJECT/run_benchmark/lra-files
# $PARALLEL -j 1 --timeout 200 $PROG3 :::: $PROJECT/run_benchmark/lra-solved-mutable-files-part2
$PARALLEL -j 5 --timeout 200 $PROG4 :::: $PROJECT/run_benchmark/finished_training
