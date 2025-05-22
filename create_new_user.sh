#!/bin/bash

username="$1"
clearpass="$2"

if [ -z "$username" -o -z "$clearpass" ] ; then
    echo "Supply username and clearpass"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
  echo "Error: This script must be run as root"
  exit 1
fi

if  grep -w -q $username /etc/passwd ; then
    echo "Huh! $username seems to exist?"
    exit 1
fi

primary_ip=$(ip -j -4 addr show dev $(ip route show | grep default | grep -oP 'dev \K\S+') | jq -r '.[0].addr_info[0].local')

cryptpass=$(python3 -c 'import crypt;print(crypt.crypt("'"$clearpass"'"))' 2> /dev/null)

useradd -m -p $cryptpass -s /bin/bash ${username}

cat <<EOF
User has been added. Details:

server: $primary_ip
username: $username
password: $clearpass

Its recommended to change the password on login
using passwd
EOF

