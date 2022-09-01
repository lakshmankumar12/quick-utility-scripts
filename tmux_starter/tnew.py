#!/usr/bin/python

import subprocess
import argparse
import sys
import re
import copy

common_functions = '''
ifaddr() {
    ip addr show | awk '/^[[:space:]]+inet / {print $NF ": " $2}' | grep "$1"
}
ilshow () {
    ip link show | awk '/^[0-9]+:/{id=$1;link=$2;if(match($0,/master [[:alnum:]-]+/)){link=link " " substr($0,RSTART,RLENGTH)} getline;
                print id " " link " " $0}' | grep "$1"
}
'''
magma_common_functions = '''
it() {
    cd $MAGMA_ROOT/lte/gateway/python/integ_tests
}
'''
testvm_functions = '''
rt() {
    make integ_test TESTS=s1aptests/${1#s1aptests/}
}
'''
agw_functions='''
dumpflows() {
    venvsudo pipelined_cli.py debug display_flows | awk '{match($2,"[[:digit:].]+",r);printf "%20s %sNL",r[0],$0}' | sort -n -r | cut -c23-
}
stopstart() {
    sudo service magma@* stop
    sudo service magma@magmad restart
    sudo service sctpd restart
}
state() {
    echo "----------mob-cli-list-allocated-ips--------"
    mobility_cli.py list_allocated_ips
    echo "----------mob-cli-get-subscriber-table------"
    mobility_cli.py get_subscriber_table
    echo "----------subscriber-cli-list-------"
    subscriber_cli.py list
    echo "----------redis-mme-nas-state-------"
    state_cli.py parse mme_nas_state
    echo "----------redis-s1ap-imsi-map-------"
    state_cli.py parse s1ap_imsi_map
    echo "----------redis-imsi-keys------------"
    state_cli.py keys IMSI | grep -v directory
    echo "----------"
}
flush() {
    echo "Flushing redis-cli -p 6380 FLUSHALL"
    redis-cli -p 6380 FLUSHALL
    echo "clearing subscriber_cli"
    subscriber_cli.py list | while read i ; do subscriber_cli.py delete $i ; done
}
'''

def prepup_bashfunctions(cmd):
    cmd = re.sub("\$","\\$",cmd)
    cmd = re.sub('"','\\"',cmd)
    cmd = re.sub('NL','''"'\\\\n'"''',cmd)
    cmd = 'source <(echo "%s")'%(cmd)
    return cmd

all_functions={}
all_functions['common'] = common_functions
all_functions['magma_common'] = magma_common_functions
all_functions['testvm'] = testvm_functions
all_functions['agw'] = agw_functions

for i in all_functions:
    all_functions[i] = prepup_bashfunctions(all_functions[i])

magma_agw   = [
                "ssh agwvm",
                "magtivate",
                all_functions['common'],
                all_functions['magma_common'],
                all_functions['agw']
            ]
magma_test  = [
                "ssh testvm",
                "magtivate",
                all_functions['common'],
                all_functions['magma_common'],
                all_functions['testvm'],
            ]
magma_test2 = copy.deepcopy(magma_test)
magma_test2[1] = "test2vm"
magma_trf   = [
                "sshmgm",
                "trfvm",
                all_functions['common'],
                all_functions['magma_common'],
            ]
hostvm      = [
                "ssh hostvm",
                "lgw",
                all_functions['common'],
            ]
debbuild   = copy.deepcopy(hostvm)
debbuild[0] = "ssh debbuild"
bare        = [
                "sshbare",
                all_functions['common'],
            ]
tr0build    = [
                "ssh tr0build",
                all_functions['common'],
            ]
tr0golden   = [
                "ssh tr0golden",
                all_functions['common'],
            ]
gxc17       = [
                "ssh gxcadmin@172.26.12.66",
                all_functions['common'],
            ]

known_commands = {}
known_commands["agw"]=magma_agw
known_commands["test"]=magma_test
known_commands["test2"]=magma_test2
known_commands["trf"]=magma_trf
known_commands["hostvm"]=hostvm
known_commands["debbuild"]=debbuild
known_commands["tr0build"]=tr0build
known_commands["bare"]=bare
known_commands["gxc17"]=gxc17
known_commands["tr0golden"]=tr0golden

def print_known_machines():
    print ("Known machines:")
    for n,m in enumerate(known_commands,1):
        print ("%3d. %s"%(n,m))

def setup_tmux_window(commands, target_pane):
    for cmd in commands:
        subprocess.run(["tmux", "send-keys", "-t", target_pane, cmd])
        subprocess.run(["tmux", "send-keys", "-t", target_pane, "\r"])
    subprocess.run(["tmux", "send-keys", "-t", target_pane, "printf '\\033c'\r"])

def create_window(title):
    pane_id = subprocess.check_output("tmux new-window -n '%s' -P -F '#{pane_id}'"%(title), shell=True).strip()
    return pane_id

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--newwin",  help="Create new window", action="store_true")
    parser.add_argument("machine",  help="machine to setup")

    options = parser.parse_args()

    return options

def verify_args(options):
    # For now only entertain known machines
    if not options.machine in known_commands:
        print ("Unknown machine to login to: %s"%options.machine)
        print_known_machines();
        sys.exit(1)

def main():
    options = parse_args()
    verify_args(options)
    title = options.machine
    if options.newwin:
        pane = create_window(title)
    else:
        pane = subprocess.check_output("tmux display-message -p '#{pane_id}'", shell=True).strip()
        subprocess.run("tmux rename-window '%s'"%(title), shell=True)

    commands = known_commands[options.machine]

    setup_tmux_window(commands, pane)

main()

