#!/bin/bash

git rev-parse HEAD > /dev/null
if [ $? -eq 0 ] ; then
    git ls-files
else
    ## .branch-name is a file that is used
    ## when you want to move to a sub-git-repo
    ## and only list files there.
    if [ -f ".branch_name" ] ; then
        if [ -d "$(cat .branch_name)" ] ; then
            br="$(cat .branch_name)"
            cd ${br}
            git ls-files | awk -v br=${br} ' { print br "/" $0 } '
        fi
    fi
fi
