#!/usr/bin/python3

import sys
from clipboard import Clipboard
from handset.kstars import KStars as Handset
from virtualoperator import Operator

import time

clipboard = Clipboard()
handset = Handset()

if handset.is_valid():
    print(f"{handset.name} has been found.")
else:
    print("Handset not found...")
    sys.exit(1)

operator = Operator(handset, clipboard.as_grayscale())
dt = 100

while True:
    while dt>10:
        dt = operator.guide_once()
        print("\rdelta={:.1f}".format(dt), end='')
    time.sleep(3)
    dt = 10+1