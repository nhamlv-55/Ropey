#!/bin/bash

#SBATCH --time=00:30:00
#SBATCH --account=def-arie
#SBATCH --cpus-per-task=32
#SBATCH --job-name=quic
#SBATCH --mem-per-cpu=8G

DATE=$(date +%d_%m_%Y-t%H-%M-%S)
PROJECT=/ag/chc-comp18
SCRATCH=/ag/chc-comp18

OUT=$SCRATCH/out/lia.deep-space.lilla.$DATE

echo "Creating directory: $OUT"
mkdir -p $OUT

PROG=$PROJECT/run/deep-space.sh

PARALLEL=/usr/local/bin/parallel

time $PARALLEL -j 8 --ungroup --results $OUT/{/} $PROG :::: $PROJECT/run/lia-files




