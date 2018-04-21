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


class JsonModel:
    def FromJsonItem(model, jsonItem):
        if (hasattr(model._definition, "pk")):
            item, created = model.get_or_create(
                **{model._definition.pk: model._definition.field_assoc[model._definition.pk]})
        else:
            item = model()
        for key in model._definition.field_assoc:
            val = model._definition.field_assoc[key]
            if (type(jsonItem[val] == list)):
                pass
            else:
                setattr(item, key, jsonItem[val])
        item.save()


class BaseModel(Model):
    def save_query(self, force_insert=False, only=None):

        query = ""
        field_dict = self.__data__.copy()
        if self._meta.primary_key is not False:
            pk_field = self._meta.primary_key
            pk_value = self._pk
        else:
            pk_field = pk_value = None
        if only:
            field_dict = self._prune_fields(field_dict, only)
        elif self._meta.only_save_dirty and not force_insert:
            field_dict = self._prune_fields(field_dict, self.dirty_fields)
            if not field_dict:
                self._dirty.clear()
                return False

        self._populate_unsaved_relations(field_dict)
        if pk_value is not None and not force_insert:
            if self._meta.composite_key:
                for pk_part_name in pk_field.field_names:
                    field_dict.pop(pk_part_name, None)
            else:
                field_dict.pop(pk_field.name, None)
            query = self.update(**field_dict).where(self._pk_expr()).sql()
        elif pk_field is None or not self._meta.auto_increment:
            query = self.insert(**field_dict).sql()
        else:
            query = self.insert(**field_dict).sql()

        result = self._meta.database.connection().cursor().mogrify(query[0],query[1])
        return result


    def GetQuery(self, data, save=True):
        query = ()
        for key in self._definition.field_assoc:
            if (not hasattr(self, key)):
                continue

            val = self._definition.field_assoc[key]
            if (not save):
                self.owner_id = 1

            data_val = data[val]
            if (type(data_val) != list):
                setattr(self, key, data[val])
            else:
                attr = getattr(self, key)
                if (issubclass(attr, BaseModel)):
                    item_id = getattr(self, self._definition.pk)
                    field_data = self._definition.field_data[key]
                    sub_model = attr
                    fk_field = getattr(sub_model, field_data.get("attributes").get("fk"))
                    sub_model.bind(self._meta.database, bind_refs=False, bind_backrefs=False)
                    _query = sub_model.delete().where(fk_field == item_id).sql()

                    query+= self._meta.database.connection().cursor().mogrify(_query[0],_query[1]),
                    subfields = field_data["fields"]
                    sub_model._definition.field_assoc = {subfields[i]["db_name"]: subfields[i]["name"] for i in
                                                         subfields}
                    for sub_data in data_val:
                        sub_item = sub_model()
                        #try:
                        if True:
                            setattr(sub_item, field_data.get("attributes").get("fk"), item_id)
                            sub_item = sub_item.GetQuery(sub_data, False)
                            query += sub_item
                        #except Exception as e:
                        #    print(e)
                            pass

        if save:
            query += self.save_query(),
        return query

    def FillAndSave(self, data, save=True):
        query = ()
        for key in self._definition.field_assoc:
            if (not hasattr(self, key)):
                continue

            val = self._definition.field_assoc[key]
            if (not save):
                self.owner_id = 1

            data_val = data[val]
            if (type(data_val) != list):
                setattr(self, key, data[val])
            else:
                attr = getattr(self, key)
                if (issubclass(attr, BaseModel)):
                    item_id = getattr(self, self._definition.pk)
                    field_data = self._definition.field_data[key]
                    sub_model = attr
                    fk_field = getattr(sub_model, field_data.get("attributes").get("fk"))
                    sub_model.bind(self._meta.database, bind_refs=False, bind_backrefs=False)
                    query=sub_model.delete().where(fk_field == item_id).execute()
                    #print(_query)
                    #query+=_query
                    subfields = field_data["fields"]
                    sub_model._definition.field_assoc = {subfields[i]["db_name"]: subfields[i]["name"] for i in
                                                         subfields}

                    for sub_data in data_val:
                        sub_item = sub_model()
                        try:
                            setattr(sub_item, field_data.get("attributes").get("fk"), item_id)
                            sub_item = sub_item.FillAndSave(sub_data, False)
                            print("qwe")
                            print(sub_item)
                            query += sub_item
                        except Exception as e:
                            print("ewq")
                            print(e)
                            pass

        if save:
            self.save()
        return query

    class Meta:
        pass


class Chest(BaseModel):
    id = IntegerField()
    name = CharField()
    chest_group_id = IntegerField()

    class _definition:
        pass

    class Meta:
        pass


class Groups(BaseModel):
    name = CharField()
    id = IntegerField()
    item_count = IntegerField()
    unique = BooleanField()

    class chest_contents(BaseModel):
        owner_id = IntegerField()
        chest_group_id = IntegerField()
        boost_id = IntegerField()
        currency_id = IntegerField()
        count = IntegerField()
        chance = IntegerField()
        index = IntegerField()

        def SetData(self, data):
            _data = {
                'index': data["index"],
                'chance': data["chance"],
                'count': data["count"],
                'boost_id': None,
                'currency_id': None,
                'chest_group_id': None
            }
            if (data["id_type"] == 1):
                self.currency_id = data["item_id"]
            elif (data["id_type"] == 2):
                self.boost_id = data["item_id"]
            elif (data["id_type"] == 3):
                _data['chest_group_id'] = data["item_id"]
                self.chest_group_id = data["item_id"]


        def GetQuery(self, data, save=True):
            self.SetData(data)
            return super(Groups.chest_contents, self).GetQuery(data)


        def FillAndSave(self, data, save=True):
            self.SetData(data)
            return super(Groups.chest_contents, self).FillAndSave(data)

        class _definition:
            pass

        pass

    class _definition:
        pass
