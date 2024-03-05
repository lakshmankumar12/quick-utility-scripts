#!/bin/bash
# Run multiple parallel instances of iperf servers


usage() {
    echo "$0 -n|--num-servers -b|--base-port -r|--report-base"
    echo "   -h|--help -- other-iperf-args-as-is-passed"
    echo
    echo " options:"
    echo "  -n|--num-servers   Num of iperf instances,  default:1"
    echo "  -b|--base-port     Base port for server,    default:5000"
    echo "  -r|--report-base   Prefix for log files,    default:iperf-server"
    exit 1
}

parse_args() {
    NUM_CLIENTS=1
    SERVERIP="${pip}"
    BASE_PORT=5000
    REPORT_BASE="iperf-server"
    options=$(getopt -o hn:b:r: -l help,num-servers:,base-port:,report-base:, -n "$0" -- "$@")
    if [ $? -ne 0 ] ; then
        echo "Incorrect options provided"
        exit 1
    fi
    eval set -- "$options"
    while true; do
        opt="$1"
        shift
        case "$opt" in
        -n|--num-servers)
            NUM_SERVERS="$1"
            shift
            ;;
        -b|--base-port)
            BASE_PORT="$1"
            shift
            ;;
        -r|--report-base)
            REPORT_BASE="$1"
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

    IPERF_OPTIONS="$*"
}
parse_args "$@"


if [ -z "$mip" ] ; then
    echo "mip -- environment variable unset. Set this to the local ip of the m/c"
    exit 1
fi

echo "Options used:"
echo "NUM_SERVERS: $NUM_SERVERS"
echo "BASE_PORT: $BASE_PORT"
echo "REPORT_BASE: $REPORT_BASE"
echo "IPERF_OPTIONS: $IPERF_OPTIONS"
echo "mip: $mip"

# Run iperf multiple times
for i in $(seq 1 $NUM_SERVERS); do

    # Set server port
    server_port=$(($BASE_PORT+$i));

    # Report file includes server port
    report_file=${REPORT_BASE}-${server_port}.txt

    # Run iperf
    cmd="iperf3 -B ${mip} -s -p $server_port -i 1 $IPERF_OPTIONS &> $report_file"
    echo "Running cmd: $cmd"
    eval $cmd &
    pids[${i}]=$!
done

function cleanup {
  echo kill -9 "${pids[@]}" > /dev/null 2> /dev/null
}
trap cleanup INT TERM EXIT HUP ERR

echo "Servers started.. you can start tailing them"
echo "pids: ${pids[@]}"

for pid in ${pids[*]}; do
    wait $pid
done
