#! /usr/bin/env python
# coding: utf8
import sys
import json
import io
import os
import csv
from urllib import request, parse

from peewee import *
from playhouse.db_url import connect


#def GetDB():
#    from Utils.ConfigUploader import DB
#    return DB


class JsonModel:
    def __init__(self):
        pass
    def FromJsonArray(model,data):
        for d in data:
            JsonModel.FromJsonItem(model,data)

    def FromJsonItem(model,jsonItem):
        if (hasattr(model._definition,"pk")):
            item, created = model.get_or_create(**{model._definition.pk : model._definition.field_assoc[model._definition.pk]})
        else:
            item = model()
        for key in model._definition.field_assoc:
            val = model._definition.field_assoc[key]
            if (type(jsonItem[val]==list)):
                pass
            else:
                setattr(item,key,jsonItem[val])
        item.save()

class BaseModel(Model):
    def FillAndSave(self,data, save = True):
        sub_items = []
        for key in self._definition.field_assoc:
            if (not hasattr(self,key)):
                continue#,data[val])


            val = self._definition.field_assoc[key]

            if (not save):
                self.owner_id = 1

            data_val = data[val]
            if (type(data_val)!=list):
                setattr(self,key,data[val])
            else:
                attr = getattr(self,key)
                if (issubclass(attr, BaseModel)):
                    item_id = getattr(self,self._definition.pk)
                    field_data = self._definition.field_data[key]
                    sub_model = attr
                    fk_field = getattr(sub_model,field_data.get("attributes").get("fk"))
                    sub_model.bind(self._meta.database, bind_refs=False, bind_backrefs=False)
                    sub_model.delete().where(fk_field == item_id).execute()

                    subfields = field_data["fields"]

                    sub_model._definition.field_assoc = {subfields[i]["db_name"]:subfields[i]["name"] for i in subfields}
                    for sub_data in data_val:
                        sub_item = sub_model()

                        try:
                            sub_item = sub_item.FillAndSave(sub_data, False)
                            setattr(sub_item,field_data.get("attributes").get("fk"),item_id)
                            sub_item.save()
                        except Exception as e:
                            print(e)
                            pass

                        #sub_item.owner_id=1
                        #print("owner_id")
                        #print(sub_item.owner_id)

                        #print("count")
                        #print(sub_item.count)
                        #print(sub_item)
                        #print(sub_item.save())
        if (save):
            self.save()
        return self

    class Meta:
        pass


class Chest(BaseModel):
    id   = IntegerField()
    name = CharField()
    chest_group_id = IntegerField()
    class _definition:
        pass
    class Meta:
        pass

class Groups(BaseModel):
    name = CharField()
    id   = IntegerField()
    item_count   = IntegerField()
    unique   = BooleanField()
    class chest_contents(BaseModel):
        owner_id  = IntegerField()
        chest_group_id = IntegerField()
        boost_id     = IntegerField()
        currency_id  = IntegerField()
        count  = IntegerField()
        chance  = IntegerField()
        index  = IntegerField()

        def FillAndSave(self,data, save = True):
            _data = {
                'index':data["index"],
                'chance':data["chance"],
                'count':data["count"],
                'boost_id':None,
                'currency_id':None,
                'chest_group_id':None
            }
            if (data["id_type"] == 1 ):
                self.currency_id=data["item_id"]
            elif (data["id_type"] == 2):
                self.boost_id=data["item_id"]
            elif (data["id_type"] == 3):
                _data['chest_group_id'] = data["item_id"]
                self.chest_group_id=data["item_id"]

            return super(Groups.chest_contents,self).FillAndSave(data)



        class _definition:
            pass

        pass
    class _definition:
        pass


"""
class Offers:
    id = IntegerField()
    name = CharField()
    price = IntegerField()
    day = IntegerField()
    duration = IntegerField()

class Location:
    id = IntegerField()
    name = CharField()
    key = CharField()
"""

"""
class Boosts(BaseModel):
    id = IntegerField()
    name = CharField()
    localisation_key = CharField()

    class _definition:
        pass
"""

"""
class Currency:
    id = IntegerField()
    pass



class Constants:
    id = IntegerField()
    pass



class Bank:
    id = IntegerField()
    pass



class Offers:
    id = IntegerField()
    pass
"""





