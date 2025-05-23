#!/bin/bash


usage() {
    echo "$0 -i infile -t timesfiles"
    echo ""
    echo " timefile should be like this"
    echo 'name1.m4a	00:00:01.000	00:00:02.000'
    echo 'name2.m4a	00:00:03.000	00:00:04.000'
}


parse_args() {
    TIMES_FILE=""
    INFILE=""
    options=$(getopt -o i:t:h -l help,infile:,,timesfile:, -n "$0" -- "$@")
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
        -t|--timesfile)
            TIMES_FILE="$1"
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

    if [ -z "$TIMES_FILE" -o -z "$INFILE" ] ; then
        echo "Must provide all of infile: $INFILE, timesfile: $TIMES_FILE"
        usage
        exit 1
    fi
    unused_args="$(echo $1 | xargs)"
    if [ -n "$unused_args" ] ; then
        echo "Ignoring remaining args: $@"
    fi
}

read_times_file() {
    arr=()
    while read line ; do
        if [ -z "$(echo $line | xargs)" ] ; then
            continue
        fi
        read -r outname start end <<< "$line"
        arr+=("$outname;$start;$end")
    done < $TIMES_FILE
}

process() {
    read_times_file

    count=1
    for item in "${arr[@]}" ; do
        cmd='IFS=";" read -r outfile start end <<< "'"$item"'"'
        eval $cmd
        echo "Writing to $outfile"
        ffmpeg -hide_banner -loglevel error -i "$INFILE" -ss $start -to $end -acodec copy $outfile
        if [ $? -ne 0 ] ; then
            exit
        fi
    done
}

parse_args "$@"
process
