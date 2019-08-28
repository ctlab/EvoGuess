#!/bin/bash

name="rokk_down"
curl -o $name/rokk.tar http://satcompetition.org/edacc/sc14/solver-download/1776
mkdir $name
tar -xf rokk.tar
