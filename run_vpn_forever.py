#!/usr/bin/python
'''
    VPN Wrapper
'''
import subprocess
import sys
import pexpect
import datetime

def expect_child(child, expect_list, intent_desc, eof_ok=0,
                    print_output=0, timeout=0, timeout_ok=0):
    ''' Wrapper on top of pexpect's child.expect([expect-list])

        intent_desc  is a string, that will printed if expect throws a exception.
        eof_ok       if non-0, returns len(expect_list)+1 when eof is hit. Otherwise eof is bad
        print_output is whether to emit child's stdout in the good-case condition
                     O/p is always stored into general_expect_failure on error
        timeout_ok   if non-0, then timeout doesn't raise Exception. You will get len(expect_list)+2 as result.
        timeout      if non-0, is passed to expect, otherwise Not. You can wait infinitely with this wrapper. Sorry.

        Note that child.before and child.after are still available to caller to consume
    '''
    try:
        error = ""
        did_timeout = 0
        if timeout:
            result = child.expect(expect_list, timeout)
        else:
            result = child.expect(expect_list)
            if result >= len(expect_list):
                #huh!
                error = "Got none of the expected result!"
    except pexpect.EOF:
        if eof_ok:
            result = len(expect_list)
        else:
            error="Eof hit:\n"
    except pexpect.TIMEOUT:
        did_timeout = 1
        if timeout_ok:
            result = len(expect_list)+1
        else:
            error="Timeout out without matches:\n"
    if print_output:
        before = child.before.decode('utf-8')
        print(before)
        if did_timeout != 1:
            after = child.after.decode('utf-8')
            print(after)
    if error:
        err_str = "Error while doing:" + intent_desc + "\n" + "Error:" + error + "\n"
        expected = ""
        for i in expect_list:
            expected += i + "\n"
        err_str += "Expected:\n" + expected + "\n"
        with open("general_expect_failure","w",encoding="utf-8") as fd:
            fd.write(err_str+child.before)
        raise Exception(err_str)
    return result

PASSWORD_FILE='/root/.vpnpasswd'
OTP_FILE='/root/.vpnkey'

USER='lakshmankumar.narayanan@gxc.io'
SERVER='172.126.76.180'
DOMAIN='GXC'


def load_from_file(file):
    ''' load value from file as a string  '''
    with open(file,'r',encoding='utf-8') as fd:
        result=fd.read().strip()
        return result

def get_password():
    ''' get password  '''
    return load_from_file(PASSWORD_FILE)

def get_otp():
    ''' get otp '''
    key = load_from_file(OTP_FILE)
    cmd = f'oathtool -b --totp {key}'
    proc = subprocess.run(cmd, shell=True, capture_output=True)
    otp = proc.stdout.strip()
    print (f"got otp of {otp}")
    return otp

def print_time():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S %Z"))

def run_forever():
    ''' run vpn client till it dies '''
    cmd=f"netExtender --no-reconnect -u '{USER}' -d {DOMAIN} {SERVER}"

    print_time()
    print ("Starting vpn")
    child = pexpect.spawn(cmd)

    passwd_list = ['Password:']
    passwd = get_password()
    op = expect_child(child, passwd_list,
                 "Waiting for first password",
                 timeout=10,
                 print_output=1)
    if op != 0:
        print ("expect failed")
        sys.exit(1)
    child.sendline(passwd)

    cert_list = ['Do you want to proceed?']
    op = expect_child(child, cert_list,
                      "Waiting for cert accept",
                      timeout=10,
                      print_output=1)
    if op != 0:
        print ("expect failed")
        sys.exit(1)
    child.sendline("y")

    post_pass_list = ['One Time Password:']
    op = expect_child(child, post_pass_list,
                 "Waiting for OTP",
                 timeout=10,
                 print_output=1)
    if op != 0:
        print ("expect failed")
        sys.exit(1)
    otp = get_otp()
    child.sendline(otp)

    post_otp_list = ['NetExtender connected successfully']
    op = expect_child(child, post_otp_list,
                 "Waiting for connect success",
                 print_output=1)
    if op != 0:
        print ("expect failed")
        sys.exit(1)

    print_time()
    print ("Brilliant connected")

    while True:
        disconnect_wait_list = ['Exiting NetExtender client']
        op = expect_child(child, post_otp_list,
                     "Waiting for disconnect",
                     print_output=1,
                     eof_ok=1,
                     timeout=3600,
                     timeout_ok=1)
        print_time()
        if op == len(disconnect_wait_list) + 1:
            print ("Cool VPN.. running for an hour now")
        elif op == len(disconnect_wait_list):
            print ("VPN exited")
            return
        else:
            print ("Disconnected")
            child.sendline("\003")


def main():
    ''' main '''
    run_forever()


main()
