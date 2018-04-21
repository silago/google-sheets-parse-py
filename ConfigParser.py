#! /usr/bin/env python
# coding: utf8
import sys
import json
import io
import os
import csv
from urllib import request, parse
from parser import schemeDefinition as sd


def Download(url, name=""):
    name = parse.quote(name)
    response = request.urlopen(url + name)
    return response



def Main(id, out):
    url = "http://docs.google.com/spreadsheets/d/" + id + "/gviz/tq?tqx=out:csv&sheet="
    if not os.path.exists(out):
        os.mkdir(out)
    print("parsing " + url)

    main_scheme = Download(url).read().decode("utf-8").splitlines()
    for row in csv.reader(main_scheme, csv.excel, delimiter=","):
        row = list(filter(None,row))
        data = None
        for x in range(1,len(row)):
            scheme = sd.SchemeDefinition(url, row, x)
            if (not scheme.Name): continue
            #scheme.Data = scheme.ParseData()
            scheme.Data = scheme.ParseData()
            try:
                if (type(scheme.Data)==list): #if []
                    data = scheme.Data if data == None else data+scheme.Data
                elif (type(scheme.Data)==dict): #if []
                    data = scheme.Data if data == None else {**data, **scheme.Data}
            except Exception as e:
                print(e)

        with io.open(os.path.join(out, scheme.Name + ".json"), 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)




    pass


if (len(sys.argv) <= 2):
    raise Exception("No url provided")
else:
    id = sys.argv[1]
    out = sys.argv[2]
    Main(id, out)
