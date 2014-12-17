#!/usr/bin/env python

import os
import subprocess
import time

# Open the channles:
os.system("ach -1 -C 'dyno-ref-chan' -m 30 -n 30000")
os.system("ach -1 -C 'state-chan' -m 30 -n 30000")
'''
pid = subprocess.Popen(args=[
    "gnome-terminal", "--command=python keyboardController.py"]).pid
print pid
time.sleep(1)


pid = subprocess.Popen(args=[
    "gnome-terminal", "--command=python dynController.py"]).pid
print pid
time.sleep(5)


pid = subprocess.Popen(args=[
    "gnome-terminal", "--command=python robotController.py"]).pid
print pid
'''
