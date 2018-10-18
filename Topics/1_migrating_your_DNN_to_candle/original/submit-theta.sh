#!/bin/bash
set -eu

# SUBMIT THETA

# The current directory
export THIS=$( readlink --canonicalize-existing $( dirname $0 ) )

TIMESTAMP=$( date +%H:%M:%S )

# Editable settings
export NODES=1
export PROJECT=ecp-testbed-01
export QUEUE=debug-cache-quad
export WALLTIME=00:15:00
export OUTPUT=$THIS/out-$TIMESTAMP.txt

# export PROGRAM=$THIS/test-print.py
# export PROGRAM=$THIS/test-keras.py
export PROGRAM=$THIS/t29res.py
#export PROGRAM=$THIS/cc_t29res.py
# Remove write permissions for job-theta to prevent accidental editing
# of generated version
touch job-theta.sh
chmod u+w job-theta.sh
m4 ../common.m4 job-theta.sh.m4 > job-theta.sh
chmod a-w,u+x job-theta.sh

# Submit!
qsub job-theta.sh
