#!/bin/zsh
set -eu

NAMES=( n-bash c-bash c-keras )

for NAME in
do
  paste procs.data $NAME.rates.data > $NAME.data
done

jwplot plot.cfg multiple.eps ${^NAMES}.data
