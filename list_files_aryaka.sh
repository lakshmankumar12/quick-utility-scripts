#!/bin/bash
#find  . -type f -not \( -path '*/import/*' -o -path '*/build.el6/*' -o -path '*/.git/*' -o -path '*/.svn/*' \) -path '*/pns_ni/*'
#find  . -type f -not \( -path '*/import/*' -o -path '*/build.el6/*' -o -path '*/.git/*' -o -path '*/.svn/*' -o -path '*/pns_ni/*' \)


git rev-parse HEAD > /dev/null
if [ $? -eq 0 ] ; then
    git ls-files
else
    if [ -f ".branch_name" ] ; then
        if [ -d "$(cat .branch_name)" ] ; then
            br="$(cat .branch_name)"
            cd ${br}
            git ls-files | awk -v br=${br} ' { print br "/" $0 } '
        fi
    fi
fi
