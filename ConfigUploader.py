import os
import sys
import json

from peewee import *
from playhouse.db_url import connect


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


env = "localhost"

if (env=="localhost"):
    db =  connect("mysql://root@localhost:/db_candy2")
    pass

if (env=="develop"):
    db =  connect("mysql://root@localhost:/db_candy2")
    pass
if (env=="production"):
    pass

class BaseModel(Model):
    class Meta:
        database =db

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









chestTemplate = {"table":"chests","pk":"id","fields":{"id":["Id",IntegerField],"name":["Name",CharField],"chest_group_id":["GroupId",IntegerField]}}

MODEL_ASSOC = {
    #'Chests':Chest,
    'Chests':chestTemplate,
}

