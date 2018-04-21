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
from models import Models as M

""" dynamoic model creator """


class ClassCreator:
    def Create(name, definition):
        properties = {}
        for k in definition:
            v = definition[k]
            if (v["type"] == "int"):
                properties[k] = IntegerField()
            if (v["type"] == "string"):
                properties[k] = CharField()
            if (v["type"] == "float"):
                properties[k] = FloatField()
            if (v["type"] == "object"):
                pass
            if (v["is_array"] == True):
                properties[k] = ClassCreator.Create(k, v["fields"])
                pass

        properties["Meta"] = type("Meta", (), {})
        properties["_definition"] = type("_definition", (), {})
        classItem = type(name, (M.BaseModel,), properties)
        return classItem


def Download(url, name):
    name = parse.quote(name)
    response = request.urlopen(url + name)
    return response


def ParseScheme(url, name=""):
    main_scheme = Download(url, name).read().decode("utf-8").splitlines()
    return [sd.SchemeDefinition(url, row) for row in csv.reader(main_scheme, csv.excel, delimiter=",")]


MODEL_ASSOC = {
    'Chests': M.Chest,
    'Groups': M.Groups,
    # 'Boosts':Models.Boosts,
}


def Main(id, path, save_query=False):
    url = "http://docs.google.com/spreadsheets/d/" + id + "/gviz/tq?tqx=out:csv&sheet="
    print("parsing " + url)
    schemes = ParseScheme(url)
    for scheme in schemes:
        result = ()
        if ("db_ignore" in scheme.Attrs):
            continue
        if (scheme.Name in MODEL_ASSOC):
            model = MODEL_ASSOC.get(scheme.Name)
        else:
            model = ClassCreator.Create(scheme.Name, {_.DbName: _.getAttributes() for _ in scheme.Fields})
        model._meta.table_name = scheme.Attrs.get("db_name", scheme.Name.lower())
        model._definition.field_assoc = {_.DbName: _.Name for _ in scheme.Fields}
        model._definition.field_data = {_.DbName: _.getAttributes() for _ in scheme.Fields}
        model._definition.pk = scheme.Attrs.get("pk", "id")
        model.bind(DB, bind_refs=False, bind_backrefs=False)
        file = open(os.path.join(path, scheme.Name + ".json"))
        json_data = json.load(file)
        for json_data in json_data:
            if (not save_query):
                _item, created= model.get_or_create( **{model._definition.pk: json_data[model._definition.field_assoc[model._definition.pk]]})
            else:
                try:
                    _item = model.get(
                        **{model._definition.pk: json_data[model._definition.field_assoc[model._definition.pk]]})
                except Exception as e:
                    print(e)
                    _item = model(**{model._definition.pk: json_data[model._definition.field_assoc[model._definition.pk]]})
                    _ = _item.save_query(force_insert=True)
                    result += (_,)

            # item, created = model.get_or_create(**{model._definition.pk : json_data[model._definition.field_assoc[model._definition.pk]]})
            item = _item

            if (save_query):
                result += item.GetQuery(json_data)
                for i in item.GetQuery(json_data):
                    print(i)
            else:
                r = item.FillAndSave(json_data)


name = sys.argv[1]
path = sys.argv[2]
connection_string = sys.argv[3]
save_query = False
if (len(sys.argv) >= 5 and sys.argv[4] == "true"):
    save_query = True
DB = connect(connection_string)
# DB =  connect("mysql://root@localhost:/db_candy2")
Main(name, path, save_query)
