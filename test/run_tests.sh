#!/bin/bash

declare -rx SCRIPT=${0##*/}
declare -rx less="/usr/bin/less"
declare -rx python="/usr/bin/python"


if test -z "$BASH"; then
    printf "Run this script in a Bash shell\n"
    exit 1
fi

if test ! -x "$less"; then
    printf "$SCRIPT:$LINENO Command $less is needed and not available\n"
    exit 1
fi

if test ! -x "$python"; then
    printf "$SCRIPT:$LINENO Command $python is needed and not available\n"
    exit 1
fi


echo "Running Textile2LaTeX tests..."


less ../README

python ../src/textile2latex4py.py -f textile_sample.txt

exit 0
