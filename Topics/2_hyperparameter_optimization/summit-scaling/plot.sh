#!/bin/bash
set -eu

if (( ${#} != 1 ))
then
  echo "Requires NAME"
  exit 1
fi

NAME=$1

paste procs.data $NAME.rates.data > $NAME.data

jwplot plot.cfg $NAME.{eps,data}
