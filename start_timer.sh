#!/bin/bash

start_timer() {
    time_in_minutes=$1
    success=0

    if [[ ${time_in_minutes} -le 0 ]] ; then
        echo "time_in_minutes:${time_in_minutes} is not more than 0."
        return
    fi

    time_in_seconds=$(( ${time_in_minutes}*60 ))
    paused=0
    pause_start=0
    paused_seconds=0
    paused_string=""
    echo "You can type p to pause the timer, u to unpause, a<N> to add N minutes"
    start=$(date '+%s')
    while [ 1 ] ; do
        userchoice=""
        read -t 1 userchoice
        case ${userchoice} in
            p*)
                if [[ ${paused} -eq 0 ]] ; then
                    paused=1
                    pause_start=$(date '+%s')
                fi
                ;;
            u*)
                if [[ ${paused} -eq 1 ]] ; then
                    paused=0
                    now=$(date '+%s')
                    pause_elapsed=$(( ${now} - ${pause_start} ))
                    paused_seconds=$(( ${paused_seconds} + ${pause_elapsed} ))
                    paused_string=""
                fi
                ;;
            a*)
                to_add=${userchoice:1}
                if [[ ${to_add} -gt 0 ]] ; then
                    echo "Adding ${to_add} minutes"
                    time_in_minutes=$(( ${time_in_minutes} + ${to_add} ))
                    time_in_seconds=$(( ${time_in_seconds} + ( ${to_add} * 60 ) ))
                fi
                ;;
            q*)
                return
                ;;
            *)
                ;;
        esac
        now=$(date '+%s')
        if [[ ${paused} -eq 0 ]] ; then
            elapsed=$(( ${now} - ${start} - ${paused_seconds}))
        else
            pause_elapsed=$(( ${now} - ${pause_start} ))
            paused_seconds_so_far=$(( ${paused_seconds} + ${pause_elapsed} ))
            paused_print_min=$(( ${paused_seconds_so_far} / 60 ))
            paused_print_sec=$(( ${paused_seconds_so_far} % 60 ))
            paused_string=$(printf "Paused: %3d:%02d" ${paused_print_min} ${paused_print_sec})
        fi
        elapsed_min=$(( $elapsed / 60 ))
        elapsed_sec=$(( $elapsed % 60 ))
        printf "\rElapsed %3d:%02d of %3d:00 %s" ${elapsed_min} ${elapsed_sec} ${time_in_minutes} "${paused_string}"
        if [[ ${elapsed} -ge ${time_in_seconds} ]] ; then
            echo
            success=1
            return
        fi
    done
}

usage() {
    echo 'start_timer.sh -t|--timer <n mins> -m|--message "your message"'
    exit 1
}
timer=0
message=""
while [[ $# > 0 ]] ; do
    key="$1"
    shift 1
    case $key in
        -t|--timer)
            timer="$1"
            shift
            ;;
        -m|--message)
            message="$1"
            shift
            ;;
        *)
            usage
        ;;
    esac
done

if [[ ${timer} -le 0 ]] ; then
    echo "Missing timer value"
    usage
fi
if [[ -z "${message}" ]] ; then
    echo "Missing message"
    usage
fi

start_timer ${timer}
if [[ ${success} -eq 1 ]] ; then
    /usr/bin/osascript -e 'tell application "System Events" to display dialog "Timer Expired: '"${message}"'" with icon note'
    exit 0
fi
exit 1
