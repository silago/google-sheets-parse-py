#! /usr/bin/env python
# coding: utf8

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
