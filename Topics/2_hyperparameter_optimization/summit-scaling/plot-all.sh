#!/bin/sh
set -eu

for N in n-bash c-bash c-keras
do
  ./plot.sh $N
done
