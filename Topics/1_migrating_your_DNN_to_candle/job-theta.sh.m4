#!/bin/bash -l
ifelse(getenv_nospace(PROJECT), `',,#COBALT -A getenv_nospace(PROJECT)
)ifelse(getenv_nospace(QUEUE), `',,#COBALT -q getenv(QUEUE)
)#COBALT -n getenv(NODES)
#COBALT -t getenv(WALLTIME)
#COBALT --cwd getenv(THIS)
#COBALT -o getenv_nospace(OUTPUT)
#COBALT -e getenv_nospace(OUTPUT)

# JOB THETA
# The COBALT directives must be at the top of the file

echo
echo "JOB: Starting ..."

echo "JOB: alps "
module load alps

set -eu

module load miniconda-3.6/conda-4.4.10
export PYTHON=$( which python )
echo PYTHON=$PYTHON

THIS=getenv(THIS)
cd $THIS

PROGRAM=getenv(PROGRAM)

export KMP_BLOCKTIME=0
export KMP_SETTINGS=1
export KMP_AFFINITY="granularity=fine,verbose,compact,1,0"
export NUM_INTER_THREADS=1
export NUM_INTRA_THREADS=128
export OMP_NUM_THREADS=128

aprun -n 1 \
      -cc none \
      -e LD_LIBRARY_PATH=$LD_LIBRARY_PATH \
      -e PYTHON=$PYTHON \
      -e THIS=$THIS \
      -e PROGRAM=$PROGRAM \
      $THIS/task.sh

echo "JOB: Complete."

# Local Variables:
# mode: m4;
# End:
