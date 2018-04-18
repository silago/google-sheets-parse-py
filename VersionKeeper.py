#! /usr/bin/env python
import sys

def Keep(version, file):
    pass


def Main(version, files):
    for f in files: Keep(version, f)

if (len(sys.argv)<=2):
    print("No files provided")
else:
    version = sys.argv[1]
    files = sys.argv[2:]
    Main(version, files)
