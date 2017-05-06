#!/bin/bash

pwdir=$(pwd)

for i in $(ls -1 "$@") ; do 
  echo ${pwdir}/$i
done
