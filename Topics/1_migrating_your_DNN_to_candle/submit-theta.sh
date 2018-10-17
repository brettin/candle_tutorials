#!/bin/bash
set -eu

# SUBMIT THETA

export THIS=$( readlink --canonicalize-existing $( dirname $0 ) )

TIMESTAMP=$( date +%H:%M:%S )

export NODES=1
export PROJECT=ecp-testbed-01
export QUEUE=debug-cache-quad
export WALLTIME=00:05:00
export OUTPUT=$THIS/out-$TIMESTAMP.txt

# export PROGRAM=$THIS/test-print.py
# export PROGRAM=$THIS/test-keras.py
export PROGRAM=$THIS/t29res.py

m4 common.m4 job-theta.sh.m4 > job-theta.sh
chmod u+x job-theta.sh

qsub job-theta.sh
