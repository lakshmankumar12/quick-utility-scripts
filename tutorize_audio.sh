#!/bin/bash


usage() {
    echo "$0 -i infile -o outfile -t timesfiles"
    echo ""
    echo " timefile should be like this"
    echo '00:00:01.000	00:00:02.000'
    echo '00:00:03.000	00:00:04.000'
}


parse_args() {
    TIMES_FILE=""
    INFILE=""
    OUTFILE=""
    options=$(getopt -o i:o:t:h -l help,infile:,outfile:,timesfile: -n "$0" -- "$@")
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

read_times_file() {
    arr=()
    while read line ; do
        if [ -z "$(echo $line | xargs)" ] ; then
            continue
        fi
        read -r start end <<< "$line"
        arr+=("$start;$end")
    done < $TIMES_FILE
}

process() {
    read_times_file

    rm -f .snip*m4a

    count=1
    for item in "${arr[@]}" ; do
        cmd='IFS=";" read -r start end <<< "'"$item"'"'
        eval $cmd
        outfile=$(printf ".snip%03d.m4a" $count)
        count=$((count + 1))
        echo "Writing to $outfile"
        ffmpeg -hide_banner -loglevel error -i $INFILE -ss $start -to $end -acodec copy $outfile
        if [ $? -ne 0 ] ; then
            exit
        fi
    done
    count=$((count - 1))

    echo "We have $count snips in total"
    rm .inlist.txt

    for i in $(seq 1 ${count}) ; do
        outfile=$(printf ".snip%03d.m4a" $i)
        for j in $(seq 1 3) ; do
            echo "file $outfile" >> .inlist.txt
        done
    done

    rm -f $OUTFILE
    echo "concatenating"
    ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i .inlist.txt -c copy $OUTFILE
}

parse_args "$@"
process
