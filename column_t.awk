#!/usr/bin/awk -f
# pipe_table_format.awk
#
# ### invoke as
# cat your_input | awk -f <this-file> -F'|' -v sep=";" > output

BEGIN {
    # Default separator is pipe if not provided
    if (!sep) sep = "|"
}

{
    # Store all lines
    lines[NR] = $0
    # Calculate max widths
    for(i=1; i<=NF; i++) {
        if(length($i) > width[i]) width[i] = length($i)
    }
    if(NF > maxfields) maxfields = NF
}

END {
    # Print all lines with proper formatting
    for(linenum=1; linenum<=NR; linenum++) {
        split(lines[linenum], fields, "|")
        for(i=1; i<=maxfields; i++) {
            printf "%-*s", width[i], fields[i]
            if(i < maxfields) printf "%s", sep
        }
        print ""
    }
}
