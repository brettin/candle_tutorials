#!/bin/bash

echo TASK

set -x
pwd
$PYTHON $PROGRAM --run_id=2epoch
