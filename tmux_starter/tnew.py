#!/usr/bin/python

import subprocess
import argparse
import sys

ifaddr = '''source <(printf "ifaddr() {\\n ip addr show | awk ' /^[0-9]+:/ { ifname=\$2   } /^[  ]+inet / { print ifname \\" \\" \$2   } ' | grep \\"\$1\\" \\n} ")'''
ilshow = '''source <(printf "ilshow() {\\n ip link show | awk ' /^[0-9]+:/ { id=\$1; link=\$2; getline; print id \\" \\" link \\" \\" \$0   } ' | grep \\"\$1\\" \\n} ")'''
it_test = '''source <(printf "it() {\\n cd \$MAGMA_ROOT/lte/gateway/python/integ_tests\\n} ")'''
# ${${a}#s1ap/}
run_test = '''source <(printf "rt() {\\n t=\$1;make integ_test TESTS=s1aptests/\${t#s1aptests/} \\n}  ")'''

magma_agw   = [
                "sshmgm",
                "agw",
                "magtivate",
                ifaddr,
                ilshow
            ]
magma_test  = [
                "sshmgm",
                "testvm",
                "magtivate",
                ifaddr,
                ilshow,
                it_test,
                run_test,
                "it"
            ]
magma_trf   = [
                "sshmgm",
                "trfvm",
                ifaddr,
                ilshow
            ]
hostvm      = [
                "sshmgm",
                "lgw",
                ifaddr,
                ilshow
            ]

known_commands = {}
known_commands["agw"]=magma_agw
known_commands["test"]=magma_test
known_commands["trf"]=magma_trf
known_commands["hostvm"]=hostvm

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

