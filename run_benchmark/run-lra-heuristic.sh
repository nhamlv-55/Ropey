#!/bin/bash

#SBATCH --time=00:30:00
#SBATCH --account=def-arie
#SBATCH --cpus-per-task=32
#SBATCH --job-name=quic
#SBATCH --mem-per-cpu=8G

DATE=$(date +%d_%m_%Y-t%H-%M-%S)
PROJECT=/home/nv3le/workspace/Doping
SCRATCH=/home/nv3le/workspace/Doping

OUT=$SCRATCH/heuristic_out/lra.deep-space.lilla.$DATE

echo "Creating directory: $OUT"
mkdir -p $OUT

PROG=$PROJECT/run_benchmark/heuristic_run.sh

PARALLEL=/usr/bin/parallel

# time $PARALLEL -j 8 --dryrun --ungroup --results $OUT/{/} $PROG :::: $PROJECT/run_benchmark/lra-files
echo "$PARALLEL -j 32 --ungroup --results $OUT/{/} $PROG :::: $PROJECT/run_benchmark/lra-files"
$PARALLEL -j 32 --ungroup --results $OUT/{/} $PROG :::: $PROJECT/run_benchmark/lra-files




