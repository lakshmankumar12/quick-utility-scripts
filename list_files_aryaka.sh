#!/bin/bash
find  . -type f -not \( -path '*/import/*' -o -path '*/build.el6/*' -o -path '*/.git/*' \)
