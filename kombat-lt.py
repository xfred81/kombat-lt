#!/usr/bin/python3

import sys
from clipboard import Clipboard
from handset.kstars import KStars as Handset
from virtualoperator import Operator

import time

config = {}

def my_input(label: str, default: float):
    r = input(f"{label} (default: {default})")
    if r == '':
        r = default

    return r

config['desired_dt'] = int(my_input("Desired guiding precision in pixels", 10))
config['press_delay'] = float(my_input("Wait time in seconds after pressing button", 2))

clipboard = Clipboard()
handset = Handset()

if handset.is_valid():
    print(f"{handset.name} has been found.")
else:
    print("Handset not found...")
    sys.exit(1)

operator = Operator(handset, clipboard.as_grayscale(), config)
dt = config['desired_dt']+1

while True:
    while dt>config['desired_dt']:
        dt = operator.guide_once()
        print("\rdelta={:.1f}   ".format(dt), end='')
    time.sleep(3)
    dt = config['desired_dt']+1