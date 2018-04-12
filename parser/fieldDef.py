#! /usr/bin/env python
# coding: utf8

class FieldDef:
    def __init__(self, input_line):
        self.raw_def = input_line
        at_lines = input_line.split("@")
        line = at_lines[-1]
        parts = line.split("-")
        self.Comment = parts[1] if (len(parts) > 1) else ""
        data = parts[0].split(" ")
        self.Name = data[0]
        self.DbName= at_lines[0] if len(at_lines)>1 else self.Name
        self.Type = data[1]
        self.IsArray = "[]" in data
        self.Attributes = {}
        self.Fields = []
        if self.Type == "object":
            self.Fields = [FieldDef(f.strip()) for f in input_line[input_line.index("{")+1:input_line.index("}")].split(",")]
            if "(" in input_line:
                self.Attributes = { _[0]:_[1] for _ in  [f.strip().split("=") for f in input_line[input_line.index("(")+1:input_line.index(")")].split(",")]}
        self.Params = data[2:] if (len(parts) > 2) else ""

    def getAttributes(self):
        return {
            'name':self.Name,
            'db_name':self.DbName,
            'type':self.Type,
            'is_array':self.IsArray,
            'attributes':self.Attributes,
            'fields':{_.Name : _.getAttributes() for _ in self.Fields}
        }
