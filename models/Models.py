#! /usr/bin/env python
# coding: utf8
import sys
import json
import io
import os
import csv
from urllib import request, parse


def GetDB():
    from Utils.ConfigUploader import DB
    return DB


class BaseChestModel(Model):gtgt
    def Fill(self):
        pass

class Chest(Model):
    id   = IntegerField()
    name = CharField()
    chest_group_id = IntegerField()

    class Meta:
        pk          = 'id'
        field_assoc = {'id':'Id','name':'Name','chest_group_id':'ChestGroup'}
        database  = GetDB()




