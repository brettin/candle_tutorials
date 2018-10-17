#!/bin/bash
#COBALT -n 2 
#COBALT -t 1:00:00
#COBALT -q debug-cache-quad --attrs mcdram=cache:numa=quad
#COBALT -A R.candle

#submisstion script for running tensorflow_mnist with horovod

echo "Running Cobalt Job $COBALT_JOBID."

#Loading modules

module load datascience/tensorflow-1.10
module load datascience/horovod-0.13.11
module load datascience/keras-2.2.2

PROC_PER_NODE=4

aprun -n $(($COBALT_JOBSIZE*$PROC_PER_NODE)) -N $PROC_PER_NODE \
    -j 2 -d 32 -cc depth \
    -e OMP_NUM_THREADS=32 \
    -e KMP_BLOCKTIME=0 \
    python t29res.py >& t29res.out


#-d means distance between nearby MPI ranks. 
#-j number of threads per core
# In this setup, I set two threads per core. In total we have 128 threads on the KNL node. I set 4 MPI ranks, 16 OpenMP threads per rank.


