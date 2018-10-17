#!/bin/bash

echo TASK

set -x
pwd
$PYTHON $THIS/test-keras.py
