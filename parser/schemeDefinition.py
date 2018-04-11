#! /usr/bin/env python
# coding: utf8
import csv
from urllib import request, parse
from . import fieldDef

def Download(url, name):
    name = parse.quote(name)
    response = request.urlopen(url + name)
    return response


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
                self.Fields += fieldDef.FieldDef(l),

        headLines = int(scheme[0].split(" ")[1])
        data = self.Data.read().decode("utf-8").splitlines()
        self.Data = self.ParseData(headLines, data)

    def ParseData(self, headlines, data):
        def SetType(type, item):
            if item is None:
                return item
            if type == "float":
                return float(item) if item != "" else float(0)
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
