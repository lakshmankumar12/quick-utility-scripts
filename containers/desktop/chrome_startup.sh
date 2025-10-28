#!/bin/bash
set -e

# 默认参数
NOVNC_PORT="${PORT:-6080}"
NOVNC_PASSWORD="${PASSWORD:-novncpass}"
SSL_ENABLE="${SSL_ENABLE:-false}"
SSL_CERT_PATH="${SSL_CERT_PATH:-/certs/fullchain.pem}"
SSL_KEY_PATH="${SSL_KEY_PATH:-/certs/privkey.pem}"

echo "Starting supervisord..."

cp /usr/share/novnc/vnc.html /usr/share/novnc/index.html
echo "Start setup password"
x11vnc -storepasswd "$NOVNC_PASSWORD" /tmp/vnc.pass

ARCH=$(dpkg --print-architecture)
if [ "$ARCH" = "amd64" ]; then
    CHROME_CMD="/usr/bin/google-chrome-stable"
elif [ "$ARCH" = "arm64" ]; then
    CHROME_CMD="/usr/bin/chromium"
else
    echo "Unsupported arch: $ARCH"
    exit 1
fi
# 替换 supervisord.conf 中 chrome 的 command 行
# with proxy
sed -i "s|command=.*chrome.*|command=$CHROME_CMD --no-sandbox --disable-infobars --disable-crash-reporter --disable-fre --no-first-run --disable-default-apps --no-default-browser-check --disable-gpu --restore-last-session --remote-debugging-port=9222 --user-data-dir=/config --disable-dev-shm-usage --display=:99 --window-size=1280,1024 --proxy-server=\"socks5://tor-proxy:9050\" about:blank|" /etc/supervisor/supervisord.conf
# without proxy
#sed -i "s|command=.*chrome.*|command=$CHROME_CMD --no-sandbox --disable-infobars --disable-crash-reporter --disable-fre --no-first-run --disable-default-apps --no-default-browser-check --disable-gpu --restore-last-session --remote-debugging-port=9222 --user-data-dir=/config --disable-dev-shm-usage --display=:99 --window-size=1280,1024 about:blank|" /etc/supervisor/supervisord.conf

# 修改 supervisord.conf中novnc命令根据是否启用SSL
if [ "$SSL_ENABLE" = "true" ] && [ -f "$SSL_CERT_PATH" ] && [ -f "$SSL_KEY_PATH" ]; then
    echo "Starting noVNC with SSL on port $NOVNC_PORT"
    sed -i "s|command=.*novnc.*|command=/usr/bin/websockify --web /usr/share/novnc/ --cert=$SSL_CERT_PATH --key=$SSL_KEY_PATH --ssl-only $NOVNC_PORT localhost:5900|" /etc/supervisor/supervisord.conf
else
    echo "Starting noVNC without SSL on port $NOVNC_PORT"
    sed -i "s|command=.*novnc.*|command=/usr/bin/websockify --web /usr/share/novnc/ $NOVNC_PORT localhost:5900|" /etc/supervisor/supervisord.conf
fi
exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
