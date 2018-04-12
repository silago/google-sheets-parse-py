#! /usr/bin/env python
# coding: utf8

import os
import sys
import json

from peewee import *
from playhouse.db_url import connect

import sys
import json
import io
import os
import csv
from urllib import request, parse
from parser import schemeDefinition as sd

"""
def Main(name, path):

    file = open(path)
    json_data = json.load(file)
    creator = ClassCreator(name,MODEL_ASSOC[name])
    creator.LoadItems(json_data)

if (len(sys.argv) <= 2):
    raise Exception("No url provided")
else:

    name = sys.argv[1]
    path = sys.argv[2]
    Main(name, path)
"""

env = "localhost"

if (env=="localhost"):
    DB =  connect("mysql://root@localhost:/db_candy2")
    pass

if (env=="develop"):
    DB =  connect("mysql://root@localhost:/db_candy2")
    pass
if (env=="production"):
    pass

class BaseModel(Model):
    class Meta:
        database = DB

""" mdynamoic model creator """
class ClassCreator:
    def __init__(self,name,definition):
        properties = {}
        for k in definition["fields"]:
            v = definition["fields"][k]
            properties[k]=v[1]()

        self.classItem  = type(name,(BaseModel,),properties)
        self.definition = definition

    def LoadItems(self, data):
        for jsonItem in data:
            #item = self.classItem.get_or_create(**{"id": 0})
            item, created = self.classItem.get_or_create(**{self.definition["pk"] : jsonItem[self.definition["fields"][self.definition["pk"]][0]]})
            for k in self.definition["fields"]:
                v = self.definition["fields"][k][0]
                setattr(item,k,jsonItem[v])
            item.save()

def GetJsonData():
    pass










def Download(url, name):
    name = parse.quote(name)
    response = request.urlopen(url + name)
    return response

def ParseScheme(url, name=""):
    main_scheme = Download(url, name).read().decode("utf-8").splitlines()

    return [sd.SchemeDefinition(url, row) for row in csv.reader(main_scheme, csv.excel, delimiter=",")]

def Main(id):
    url = "https://docs.google.com/spreadsheets/d/" + id + "/gviz/tq?tqx=out:csv&sheet="
    print("parsing " + url)
    schemes = ParseScheme(url)

name = sys.argv[1]
Main(name)

""""
chestTemplate = {"table":"chests","pk":"id","fields":{"id":["Id",IntegerField],"name":["Name",CharField],"chest_group_id":["GroupId",IntegerField]}}

MODEL_ASSOC = {
    #'Chests':Chest,
    'Chests':chestTemplate,
}

"""
