#!/usr/bin/python
'''
    VPN Wrapper
'''
import subprocess
import sys
import pexpect
import datetime
import threading
from time import sleep

PASSWORD_FILE='/root/.vpnpasswd'
OTP_FILE='/root/.vpnkey'
PING_FILE='/root/.vpn_ping_ip'

USER='lakshmankumar.narayanan@gxc.io'
SERVER='172.126.76.180'
DOMAIN='GXC'
PROTOCOL='wireguard'
#PROTOCOL='sslvpn'

global_status = {}
global_status['keep_going'] = True
global_status['connected'] = False
global_status['ping_status'] = True

def expect_child(child, expect_list, intent_desc, eof_ok=0,
                    print_output=0, timeout=0, timeout_ok=0,
                    flush_buffers=0):
    ''' Wrapper on top of pexpect's child.expect([expect-list])

        intent_desc  is a string, that will printed if expect throws a exception.
        eof_ok       if non-0, returns len(expect_list)+1 when eof is hit. Otherwise eof is bad
        print_output is whether to emit child's stdout in the good-case condition
                     O/p is always stored into general_expect_failure on error
        timeout_ok   if non-0, then timeout doesn't raise Exception. You will get len(expect_list)+2 as result.
        timeout      if non-0, is passed to expect, otherwise Not. You can wait infinitely with this wrapper. Sorry.
        flush_buffers  if set, child.before is cleared off, for timeouts.
    '''
    try:
        error = ""
        did_timeout = 0
        did_eof = 0
        if timeout:
            result = child.expect(expect_list, timeout)
        else:
            result = child.expect(expect_list)
            if result >= len(expect_list):
                #huh!
                error = "Got none of the expected result!"
    except pexpect.EOF:
        did_eof = 1
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
        if child.before:
            before = child.before.decode('utf-8')
            print(before)
        if did_timeout != 1 and did_eof != 1:
            if child.after:
                after = child.after.decode('utf-8')
                print(after)
    if error:
        err_str = "Error while doing:" + intent_desc + "\n" + "Error:" + error + "\n"
        expected = ""
        for i in expect_list:
            expected += i + "\n"
        err_str += "Expected:\n" + expected + "\n"
        with open("/tmp/vpn_client_general_expect_failure","w",encoding="utf-8") as fd:
            fd.write(err_str+str(child.before))
        raise Exception(err_str)
    else:
        if did_timeout:
            if child.before:
                child.expect(r'.+')
    return result

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
    otp = proc.stdout.decode('utf-8').strip()
    print (f"got otp of {otp}")
    return otp

def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S %Z")

def get_ping_ip():
    return load_from_file(PING_FILE)

def ping_thread(discard_args):
    ping_ip = get_ping_ip()
    cmd=f"ping -c 3 {ping_ip}"
    last_ping_time = datetime.datetime.now()
    while True:
        global_status['ping_event'].wait(timeout=10)
        global_status['ping_event'].clear()
        if not global_status['keep_going']:
            break
        if global_status['connected']:
            proc = subprocess.run(cmd, shell=True, capture_output=True)
            op = proc.stdout.decode('utf-8')
            if proc.returncode == 0:
                success = True
                global_status['ping_status'] = True
            else:
                success = False
                global_status['ping_status'] = False
            print (f"{now_str()} Ran ping cmd:{cmd}, ok:{success}")
            if not success:
                print (op)


def run_forever():
    ''' run vpn client till it dies '''
    cmd=f"netExtender --no-reconnect -u '{USER}' -d {DOMAIN} -T {PROTOCOL} {SERVER}"

    print (f"{now_str()} Starting vpn with cmd: {cmd}")
    child = pexpect.spawn('/bin/bash', ['-c', cmd])

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

    post_otp_list = ['NetExtender.*connected successfully']
    op = expect_child(child, post_otp_list,
                 "Waiting for connect success",
                 timeout=20,
                 print_output=1)
    if op != 0:
        print ("expect failed")
        sys.exit(1)

    #grab more output anyway
    post_otp_list = ['Just to grab ouput']
    expect_child(child, post_otp_list,
                 "Collect all connect output",
                 timeout=2,
                 timeout_ok=1,
                 flush_buffers=1,
                 print_output=1)

    print (f"{now_str()} Connected")
    global_status['connected'] = True
    global_status['ping_status'] = True  #assume ping is okay
    global_status['ping_event'].set()
    monitor_time = datetime.datetime.now()

    while True:
        if not global_status['ping_status']:
            print ("f{now_str()}  Detected a failing ping.. Killing vpn")
            child.sendline("\003")
        try:
            disconnect_wait_list = ['Exiting NetExtender client']
            op = expect_child(child, post_otp_list,
                         "Waiting for disconnect",
                         print_output=1,
                         eof_ok=1,
                         timeout=5,
                         flush_buffers=1,
                         timeout_ok=1)
            if op == len(disconnect_wait_list) + 1:
                #timeout
                now = datetime.datetime.now()
                if now - monitor_time > datetime.timedelta(seconds=3600):
                    print (f"{now_str()} Cool VPN.. running for an hour now")
                    monitor_time = now
                continue
            elif op == len(disconnect_wait_list):
                print (f"{now_str()} VPN exited")
                return
            if op == 0:
                print (f"{now_str()} Disconnected")
            if op == 0 or global_status['keep_going'] == 0:
                child.sendline("\003")
        except KeyboardInterrupt:
            print (f"{now_str()} User pressed ^c. Stopping vpn")
            global_status['keep_going']=False
            global_status['ping_event'].set()
            child.sendline("\003")

def main():
    ''' main '''
    thr = threading.Thread(target=ping_thread, args=(None,))
    global_status['ping_event'] = threading.Event()
    thr.start()
    while global_status['keep_going']:
        global_status['connected'] = False
        run_forever()
    print ("Waiting for ping thread to finish")
    thr.join()


main()
