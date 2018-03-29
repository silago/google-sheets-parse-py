#! /usr/bin/env python
import sys
import os
from hashlib import md5

class FileStats:
    abspath = None
    relpath = None
    md5     = None
    dateMod = None
    version = None

    def getModDate(self):
        return os.path.getmtime(self.path)

    def getMd5(self):
        hash_md5 = md5()
        with open(self.abspath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""): hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def __init__(self, path, base):
        self.relpath = path
        self.abspath = os.path.join(base,path)
        self.md5  = self.getMd5()
        self.dateMod = self.getModDate()

    def __str__(self):
        return ",".join([self.relpath, self.md5, self.dateMod])


def GetStats(files,base):
    return [FileStats(filename,base) for filename in files]

def GetFiles(path):
    return [os.path.join(root,name) for root, dirs, files in os.walk(path, topdown=False) for name in files]

def Main(path):
    fileStats = GetStats(GetFiles(path),path)
    for f in fileStats:
        print(f)
        print("\n")

if (len(sys.argv)<=1):
    print("No files provided")
else:
    path = sys.argv[1]
    Main(path)
