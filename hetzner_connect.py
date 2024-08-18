#!/usr/bin/python3

from my_python_util import (
        general_expect,
        spawn_child_later_for_interaction,
        execute_cmd,
        )


class CmdState:
    def __init__(self, expect_list, desc, ok_op, next_cmd, timeout=5):
        self.expect_list = expect_list
        self.desc = desc
        self.ok_op = ok_op
        self._next_cmd = next_cmd
        self.timeout = timeout

    @property
    def next_cmd(self):
        if callable(self._next_cmd):
            return self._next_cmd()
        else:
            return self._next_cmd

def build_states():
    states = []
    states.append(CmdState(
                    desc='Initial bash prompt',
                    expect_list=[r'lakshman@lakshman-VirtualBox:'], ok_op=0,
                    next_cmd='mhb'))
    states.append(CmdState(
                    desc='Prompt from bare post mosh in',
                    expect_list=[r'lakshman@dev-alpha:'], ok_op=0,
                    next_cmd='sd'))
    states.append(CmdState(
                    desc='Prompt from dev',
                    expect_list=['lakshman@lakshmandevhetzner'], ok_op=0,
                    next_cmd='ta'))
    return states

def main():
    states = build_states()
    c = spawn_child_later_for_interaction("bash")
    c.sendline('\r');
    c.sendline('\r');

    for i in states:
        res = general_expect(c, i.expect_list, i.desc, print_output=1, timeout=i.timeout)
        if res == i.ok_op:
            if i.next_cmd is None:
                continue
            c.sendline(i.next_cmd)
        else:
            print ("didnt get ok_op:%s, but got: %s, for %s"%(i.ok_op, res, i.desc))
            sys.exit(1)

    c.interact()

if __name__ == "__main__":
    main()



