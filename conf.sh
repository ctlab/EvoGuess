#!/bin/bash

RUN=$(python3 tools/conf/conf.py "$@")
echo $RUN
sleep 1
"${RUN[@]}"
