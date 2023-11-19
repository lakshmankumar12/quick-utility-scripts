import os
import struct
import subprocess
import time
from fcntl import ioctl
from ipaddress import IPv4Address

_UNIX_TUNSETIFF = 0x400454ca
_UNIX_TUNSETPERSIST = 0x400454cb
_UNIX_IFF_TUN = 0x0001
_UNIX_IFF_TAP = 0x0002
_UNIX_IFF_NO_PI = 0x1000

### References:
### https://stackoverflow.com/a/55276723
### https://gist.github.com/abdelrahman-t/a23f57986a40f54108a71d4b91f145b2

class TUNTAPInterface:

    def __init__(self, name: str, address: IPv4Address = None, persist: bool = False, tap: bool = False):
        self._name = name
        self._address = address

        mode = _UNIX_IFF_TAP if tap else _UNIX_IFF_TUN

        # Create TUN interface.
        self._descriptor = os.open('/dev/net/tun', os.O_RDWR)
        ioctl(self._descriptor,
              _UNIX_TUNSETIFF,
              struct.pack('16sH', name.encode('ASCII'), mode | _UNIX_IFF_NO_PI)
              )

        if persist:
            ioctl(self._descriptor,
                  _UNIX_TUNSETPERSIST,
                  struct.pack('I', 1),
                  )

        if address != None:
            # Assign address to interface.
            subprocess.call(['/sbin/ip', 'addr', 'add', str(address), 'dev', name])

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> IPv4Address:
        return self._address

    def up(self) -> None:
        # Put interface into "up" state.
        subprocess.call(['/sbin/ip', 'link', 'set', 'dev', self._name, 'up'])

    def read(self, number_bytes: int) -> bytes:
        packet = os.read(self._descriptor, number_bytes)
        return packet

    def write(self, packet: bytes) -> None:
        os.write(self._descriptor, packet)


def test() -> None:
    interface = TUNTAPInterface('persist-tunnel', address=IPv4Address('10.1.0.1'), persist=1)
    interface.up()
    print ("The interface persist-tunnel is created. It will stay after the program dies")

    interface = TUNTAPInterface('persist-tap', address=IPv4Address('10.2.0.1'), persist=1, tap=True)
    interface.up()
    print ("The tap interface persist-tap is created. It will stay after the program dies")

    interface = TUNTAPInterface('custom-tunnel', address=IPv4Address('10.3.0.1'))
    interface.up()
    print ("The interface custom-tunnel is created. It will go away if this program dies")

    interface = TUNTAPInterface('custom-tap', address=IPv4Address('10.4.0.1'), tap=True)
    interface.up()
    print ("The interface custom-tap is created. It will go away if this program dies")

    time.sleep(100)

if __name__ == '__main__':
    test()
