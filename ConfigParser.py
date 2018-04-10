#! /usr/bin/env python
# coding: utf8
import sys
import json
import io
import os
import csv
from urllib import request, parse


class FieldDef:
    def __init__(self, line):
        parts = line.split("-")
        self.Comment = parts[1] if (len(parts) > 1) else ""
        data = parts[0].split(" ")
        self.Name = data[0]
        self.Type = data[1]
        self.IsArray = "[]" in data
        self.Fields = []
        if self.Type == "object":
            record = False
            line = ""
            for i in data[2:]:
                if i == "": continue
                if i == "}": break
                if i[-1] == "}":
                    line += " " + i[0:-1]
                    break
                if (record): line += " " + i
                if i[0] == "{": record = True

            self.Fields = [FieldDef(field.strip()) for field in line.split(",")]
        self.Params = data[2:] if (len(parts) > 2) else ""


class SchemeDefinition:
    def __init__(self, base, row):
        self.Fields = []
        fields = row
        self.Name = fields[0]
        self.ListName = fields[1]
        scheme = fields[2].split(";")
        if len(scheme) <= 1: return

        self.Data = Download(base, self.ListName)
        for line in scheme[1:]:
            l = line.strip()
            if l != "" and l[0] != "#":
                self.Fields += FieldDef(l),

        headLines = int(scheme[0].split(" ")[1])
        data = self.Data.read().decode("utf-8").splitlines()
        self.Data = self.ParseData(headLines, data)

    def ParseData(self, headlines, data):
        def SetType(type, item):
            if item is None:
                return item
            if type == "int":
                return int(item) if item != "" else 0
            elif type == "string":
                return str(item)
            elif type == "bool":
                return item == '"True"'

        def InArray(row, fields):

            _row = row[:]
            for f in fields:
                for i in range(f[0], f[0] + f[1]):
                    _row[i] = None
            result = "".join([r for r in _row if r != None])
            return result == ""

        items = []
        array_items = []
        a_offset = 0
        for f in self.Fields:
            if f.IsArray: array_items += [self.Fields.index(f) + a_offset, len(f.Fields)],
            if f.Type == "object": a_offset += len(f.Fields) - 1

        rows_index = 0
        for row in csv.reader(data, csv.excel, delimiter=","):
            if rows_index < headlines:
                rows_index += 1
                continue

            in_array: bool = InArray(row, array_items)
            if (not in_array): items += {},

            if (len(list(filter(None, row))) == 0): continue
            item = items[-1]

            cell_index: int = 0
            for field in self.Fields:
                if in_array == True and field.IsArray == False:
                    if field.Type == "object":
                        cell_index += len(field.Fields)
                    else:
                        cell_index += 1
                    continue

                val = row[cell_index]

                if field.Type == "none":
                    pass
                elif field.Type != "object":
                    val = SetType(field.Type, row[cell_index])
                elif field.Type == "object":
                    val = {}
                    for sub in field.Fields:
                        val[sub.Name] = SetType(sub.Type, row[cell_index])
                        cell_index += 1

                if (field.IsArray):
                    if field.Name in item:
                        item[field.Name] += val,
                    else:
                        item[field.Name] = [val, ]

                else:
                    item[field.Name] = val

                if field.Type != "object":
                    cell_index += 1
        return items


def Download(url, name):
    name = parse.quote(name)
    response = request.urlopen(url + name)
    return response


def ParseScheme(url, name=""):
    main_scheme = Download(url, name).read().decode("utf-8").splitlines()
    schemes = [SchemeDefinition(url, row) for row in csv.reader(main_scheme, csv.excel, delimiter=",")]
    return schemes


def Main(id, out):
    url = "https://docs.google.com/spreadsheets/d/" + id + "/gviz/tq?tqx=out:csv&sheet="
    print("parsing " + url)
    schemes = ParseScheme(url)
    if not os.path.exists(out):
        os.mkdir(out)
    for scheme in schemes:
        with io.open(os.path.join(out, scheme.Name + ".json"), 'w', encoding='utf8') as json_file:
            json.dump(scheme.Data, json_file, ensure_ascii=False)
    pass


if (len(sys.argv) <= 2):
    raise Exception("No url provided")
else:
    id = sys.argv[1]
    out = sys.argv[2]
    Main(id, out)
