#!/bin/bash

curl -fL -o hello-world.tar.gz \
  https://github.com/francisg22/C2HackingProj/archive/refs/heads/master.tar.gz && tar -xzf hello-world.tar.gz
curl -fL https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
/bin/python2.7 get-pip.py --user --no-setuptools --no-wheel
/bin/python2.7 -m pip --version
python2.7 -m pip install --user 'cryptography==3.3.2'


