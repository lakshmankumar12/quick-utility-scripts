#!/bin/bash
# Run multiple parallel instances of iperf client

usage() {
    echo "$0 -n|--num-clients -s|--server-ips -S|repeat-serverip"
    echo "   -c|--client-ips -C|--repeat-clientip -b|--base-port"
    echo "   -r|--report-base -d|--duration -B|--bandwidth -u|--udp -- <iperf-options>"
    echo
    echo " options:"
    echo "   -n|--num-clients      Num of iperf instances, default:1"
    echo "   -s|--server-ips       List of serverip, comma-separated"
    echo "   -S|repeat-serverip    Use the same server ip for all instances"
    echo "   -c|--client-ips       List of local-ips, comma-separated"
    echo "   -C|--repeat-clientip  Use the same local ip for all instances"
    echo "   -b|--base-port        Base port to use,    default:5000"
    echo "   -r|--report-base      Prefix for log files, default: iperf-client"
    echo "   -d|--duration         Duration to send, default:60s"
    echo "   -B|--bandwidth        Data rate, default 2M"
    echo "   -u|--udp              Use udp instead of tcp"
    exit 1
}

parse_args() {
    NUM_CLIENTS=1
    NUM_SERVERS=1
    SERVERIPS="${pip}"
    CLIENTIPS="${mip}"
    REPEAT_CLIENT_IP=""
    REPEAT_SERVER_IP=""
    BASE_PORT=5000
    REPORT_BASE="iperf-client"
    DURATION=60
    DATARATE=2M
    UDP=""
    options=$(getopt -o hn:s:Sc:Cb:r:d:B:u -l help,num-clients:,server-ips:,repeat-serverip,client-ips:,repeat-clientip,base-port:,report-base:,duration:,bandwidth:,udp -n "$0" -- "$@")
    if [ $? -ne 0 ] ; then
        echo "Incorrect options provided"
        exit 1
    fi
    eval set -- "$options"
    while true; do
        opt="$1"
        shift
        case "$opt" in
        -n|--num-clients)
            NUM_CLIENTS="$1"
            NUM_SERVERS="$1"
            shift
            ;;
        -s|--server-ips)
            SERVERIPS="$1"
            shift
            ;;
        -S|--repeat-serverip)
            REPEAT_SERVER_IP="yes"
            ;;
        -c|--client-ips)
            CLIENTIPS="$1"
            shift
            ;;
        -C|--repeat-clientip)
            REPEAT_CLIENT_IP="yes"
            ;;
        -b|--base-port)
            BASE_PORT="$1"
            shift
            ;;
        -r|--report-base)
            REPORT_BASE="$1"
            shift
            ;;
        -d|--duration)
            DURATION="$1"
            shift
            ;;
        -B|--bandwidth)
            DATARATE="$1"
            shift
            ;;
        -u|--udp)
            UDP="-u"
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

if [ -z "$CLIENTIPS" ] ; then
    echo "CLIENTIPS is empty"
    usage
fi
if [ -z "$SERVERIPS" ] ; then
    echo "SERVERIPS is empty"
    usage
fi
if [ -n "$REPEAT_CLIENT_IP" ] ; then
    client_ips=($(printf "$CLIENTIPS %.0s" $(seq 1 ${NUM_CLIENTS})))
else
    client_ips=(${CLIENTIPS//,/ })
    if [ ${#client_ips[@]} -ne ${NUM_CLIENTS} ] ; then
        echo "num of client-ips: ${#client_ips[@]} doesn't match NUM_CLIENTS: $NUM_CLIENTS"
        usage
    fi
fi
if [ -n "$REPEAT_SERVER_IP" ] ; then
    server_ips=($(printf "$SERVERIPS %.0s" $(seq 1 ${NUM_SERVERS})))
else
    server_ips=(${SERVERIPS//,/ })
    if [ ${#server_ips[@]} -ne ${NUM_SERVERS} ] ; then
        echo "num of server-ips: ${#server_ips[@]} doesn't match NUM_SERVERS: $NUM_SERVERS"
        usage
    fi
fi

echo "Options:"
echo "NUM_CLIENTS: $NUM_CLIENTS"
echo "BASE_PORT: $BASE_PORT"
echo "client_ips: ${client_ips[@]}"
echo "server_ips: ${server_ips[@]}"
echo "REPORT_BASE: $REPORT_BASE"
echo "DURATION: $DURATION"
echo "DATARATE: $DATARATE"
echo "UDP: $UDP"
echo "IPERF_OPTIONS: $IPERF_OPTIONS"


for i in $(seq 0 $((NUM_CLIENTS-1))); do

    # Set server port
    server_port=$(($BASE_PORT+$i+1));
    client_ip=${client_ips[$i]}
    server_ip=${server_ips[$i]}

    # Report file includes server ip, server port and test duration
    report_file=${REPORT_BASE}-${server_ip}-${server_port}.txt

    # Run iperf
    cmd="iperf3 -B ${client_ip} -p ${server_port} -c ${server_ip} -i 1 -t $DURATION -b $DATARATE $UDP $IPERF_OPTIONS"
    echo "Running $cmd"
    eval $cmd &> $report_file &
    pids[${i}]=$!
    sleep 1
done

function cleanup {
  echo kill -9 "${pids[@]}" > /dev/null 2> /dev/null
}
trap cleanup INT TERM EXIT HUP ERR

echo "clients started.. you can start tailing them"
echo "pids: ${pids[@]}"

for pid in ${pids[*]}; do
    wait $pid
done
