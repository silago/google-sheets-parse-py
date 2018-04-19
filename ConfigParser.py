#! /usr/bin/env python
# coding: utf8
import sys
import json
import io
import os
import csv
from urllib import request, parse
from parser import schemeDefinition as sd


def Download(url, name):
    name = parse.quote(name)
    response = request.urlopen(url + name)
    return response


def ParseScheme(url, name=""):
    main_scheme = Download(url, name).read().decode("utf-8").splitlines()
    schemes = [sd.SchemeDefinition(url, row) for row in csv.reader(main_scheme, csv.excel, delimiter=",")]
    return schemes


def Main(id, out):
    url = "http://docs.google.com/spreadsheets/d/" + id + "/gviz/tq?tqx=out:csv&sheet="
    print("parsing " + url)
    schemes = ParseScheme(url)
    if not os.path.exists(out):
        os.mkdir(out)
    for scheme in schemes:
        if (not scheme.Name): continue
        scheme.Data = scheme.ParseData()
        with io.open(os.path.join(out, scheme.Name + ".json"), 'w', encoding='utf8') as json_file:
            json.dump(scheme.Data, json_file, ensure_ascii=False)
    pass


if (len(sys.argv) <= 2):
    raise Exception("No url provided")
else:
    id = sys.argv[1]
    out = sys.argv[2]
    Main(id, out)
