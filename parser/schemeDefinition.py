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
    def __init__(self, base, row, part = 1):
        self.Fields = []
        fields = row
        self.Name = fields[0]
        self.Scheme = fields[part].split(";")
        self.Base = base
        if len(self.Scheme) <= 1: return
        header = self.Scheme[0].split(",")
        self.Attrs = {}
        for h in header:
            key, value, *(rest) = h.strip().split("=")
            self.Attrs[key]=value

        for line in self.Scheme[1:]:
            l = line.strip()
            if l != "" and l[0] != "#":
                self.Fields += fieldDef.FieldDef(l),

        self.ListName = self.Attrs.get("List")


    def ParseData(self):
        def SetType(type, item):
            if item is None:
                return item
            if type == "float":
                return float(item) if item != "" else None
            if type == "int":
                return int(item) if item != "" else None
            elif type == "string":
                return str(item)
            elif type == "bool":
                return item == '"True"'


        def InArray(row, fields, inner=False):
            _row = row[:] # _row is copy of row
            _counter = 0
            for f in fields:
                if f.IsArray:
                    for x in f.Fields:
                        if x.Type=="object":
                            for y in x.Fields: _counter+=1
                        else:
                            _counter+=1
                elif f.Type=="object":
                    for x in f.Fields:
                        if (row[_counter]): return False
                        _counter+=1
                else:
                    if (row[_counter]): return False
                    _counter+=1
            return True




            for f in fields:
                for i in range(f[0], f[0] + f[1]):
                    _row[i] = None
            result = "".join([r for r in _row if r != None])
            return result == ""

        raw_data  = Download(self.Base, self.ListName)
        headlines = int(self.Attrs.get("Header"))
        data = raw_data.read().decode("utf-8").splitlines()


        items = []
        array_items = []
        #a_offset = 0
        #for f in self.Fields:
        #    if f.IsArray: array_items += [self.Fields.index(f) + a_offset, (len(f.Fields) if f.Type=="object" else 1)],
        #    if f.Type == "object": a_offset += len(f.Fields) - 1

        rows_index = 0
        for row in csv.reader(data, csv.excel, delimiter=","):
            if rows_index < headlines:
                rows_index += 1
                continue

            in_array: bool = InArray(row, self.Fields)
            if (not in_array or len(items)==0 ):
                items += {},

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
                    # TODO:: separate to inner function
                    for sub in field.Fields:
                        if(sub.Type=="object"):
                            val[sub.Name]={}
                            for inner_sub_field in sub.Fields:
                                val[sub.Name][inner_sub_field.Name] = SetType(inner_sub_field.Type, row[cell_index])
                                cell_index+=1
                        else:
                            val[sub.Name] = SetType(sub.Type, row[cell_index])
                            cell_index += 1

                if (field.IsArray):
                    if val != None:
                        if field.Name in item:
                            item[field.Name] += val,
                        else:
                            item[field.Name] = [val, ]
                else:
                    item[field.Name] = val

                if field.Type != "object":
                    cell_index += 1


            pk_field = self.Attrs.get("pk")
            if pk_field and len(items)>1 and (items[-1].get(pk_field) == items[-2].get(pk_field)) and items[-1].get(pk_field!=None):
                curr = items[-1]
                prev = items[-2]
                for f in self.Fields:
                    if f.IsArray:
                        prev[f.Name]+=curr[f.Name]
                items=items[0:-1]


        if (self.Attrs.get("as_single")):
            items=items[0]

        as_object = self.Attrs.get("as_object")
        if (as_object):
            return {as_object:items}

        return items
