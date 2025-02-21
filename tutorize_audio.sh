#!/bin/bash


usage() {
    echo "$0 -i infile -o outfile timesfiles"
    echo ""
    echo " timefile should be like this (it will be source as-is)"
    echo 'arr+=("00:00:01.000;00:00:02.000")'
    echo 'arr+=("00:00:03.000;00:00:04.000")'
}


parse_args() {
    TIMES_FILE=""
    INFILE=""
    OUTFILE=""
    options=$(getopt -o i:o:h -l help,infile:,outfile: -n "$0" -- "$@")
    if [ $? -ne 0 ] ; then
        echo "Incorrect options provided"
        exit 1
    fi
    eval set -- "$options"
    while true; do
        opt="$1"
        shift
        case "$opt" in
        -i|--infile)
            INFILE="$1"
            shift
            ;;
        -o|--outfile)
            OUTFILE="$1"
            shift
            ;;
        -h|--help)
            usage
            ;;
        --)
            break
            ;;
        *)
            echo "Unknown option: $opt"
            usage
            ;;
        esac
    done

    TIMES_FILE="$(echo $1 | xargs)" ; shift || true

    if [ -z "$TIMES_FILE" -o -z "$INFILE" -o -z "$OUTFILE" ] ; then
        echo "Must provide all of infile: $INFILE, outfile: $OUTFILE, timesfile: $TIMES_FILE"
        usage
        exit 1
    fi
    unused_args="$(echo $1 | xargs)"
    if [ -n "$unused_args" ] ; then
        echo "Ignoring remaining args: $@"
    fi
}

process() {
    arr=()
    source $TIMES_FILE

    rm -f snip*m4a

    count=1
    for item in "${arr[@]}" ; do
        cmd='IFS=";" read -r start end <<< "'"$item"'"'
        eval $cmd
        outfile=$(printf "snip%03d.m4a" $count)
        count=$((count + 1))
        ffmpeg -i $INFILE -ss $start -to $end -acodec copy $outfile
    done

    for i in $(seq 1 $((count - 1))) ; do
        outfile=$(printf "snip%03d.m4a" $i)
        for j in $(seq 1 3) ; do
            echo "file $outfile" >> inlist.txt
        done
    done

    ffmpeg -f concat -safe 0 -i inlist.txt -c copy $OUTFILE

}

parse_args "$@"
process
