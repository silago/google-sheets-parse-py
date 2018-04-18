#! /usr/bin/env python

import sys
import os
from hashlib import md5

if (len(sys.argv)<=1):
    raise Exception("No path provided")
else:
    path = sys.argv[1]
    if (path[0]!="/" and path[0]!="~"):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),path)
    Main(path)


