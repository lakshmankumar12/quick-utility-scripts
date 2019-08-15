#!/bin/bash

usage() {
    echo "$0 <grep_pattern> <file_grep_patter> <file_with_src_list>"
    exit 1
}

if [ -z "$1" ] ; then
    usage
else
    grep_pat="$1"
    shift
fi

if [ -z "$1" ] ; then
    usage
else
    file_grep_pat="$1"
    shift
fi

if [ -z "$1" ] ; then
    usage
else
    file_list="$1"
    shift
fi

grep "${file_grep_pat}" "${file_list}" | xargs --delimiter='\n' grep -Hn "$@" ${grep_pat}
