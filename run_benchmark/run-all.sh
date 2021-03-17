#!/bin/bash

#SBATCH --time=00:30:00
#SBATCH --account=def-arie
#SBATCH --cpus-per-task=32
#SBATCH --job-name=quic
#SBATCH --mem-per-cpu=8G

DATE=$(date +%d_%m_%Y-t%H-%M-%S)
PROJECT=/home/nle/workspace/Doping
SCRATCH=/home/nle/workspace/Doping

OUT=$SCRATCH/origin_out/lra.deep-space.lilla.$DATE

echo "Creating directory: $OUT"
mkdir -p $OUT

PROG1=$PROJECT/run_benchmark/collect-data.sh
PROG2=$PROJECT/run_benchmark/generate-data.sh
PROG3=$PROJECT/run_benchmark/train.sh
PROG4=$PROJECT/run_benchmark/run-grpc-variants.sh
PROG4_P_ONLY=$PROJECT/run_benchmark/run-p-only-variants.sh
PROG4_N_ONLY=$PROJECT/run_benchmark/run-n-only-variants.sh
PROG4_RANDOM=$PROJECT/run_benchmark/run-random-variants.sh
PARALLEL=/usr/bin/parallel

TAG=$2
FILELIST=$1

echo "FILELIST:" $FILELIST
echo "TAG:" $TAG

# time $PARALLEL -j 8 --dryrun --ungroup --results $OUT/{/} $PROG :::: $PROJECT/run_benchmark/lra-files
# $PARALLEL -j 16 --results $OUT/{/} $PROG1 :::: $PROJECT/run_benchmark/$FILELIST ::: $TAG
$PARALLEL -j 32 --results $OUT/{/} $PROG2 :::: $PROJECT/run_benchmark/$FILELIST ::: $TAG
# $PARALLEL -j 4 $PROG3 :::: $PROJECT/run_benchmark/$FILELIST ::: $TAG
# $PARALLEL -j 5 --results $OUT/{/} $PROG4 :::: $PROJECT/run_benchmark/finished_training
# $PARALLEL -j 10 --results $OUT/{/} $PROG4_P_ONLY :::: $PROJECT/run_benchmark/finished_training
# sleep 10
# $PARALLEL -j 10 --results $OUT/{/} $PROG4_N_ONLY :::: $PROJECT/run_benchmark/finished_training
