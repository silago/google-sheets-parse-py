#! /usr/bin/env python
# coding: utf8
import json
import sys

#from ElementTree_pretty import prettify
from xml import etree
from xml.etree.ElementTree import (
    Element, SubElement, Comment, tostring,
    ElementTree)
from xml.etree import ElementTree as ET


"""
top = Element('top')

comment = Comment('Generated for PyMOTW')
top.append(comment)

child = SubElement(top, 'child')
child.text = 'This child contains text.'

child_with_tail = SubElement(top, 'child_with_tail')
child_with_tail.text = 'This child has regular text.'
child_with_tail.tail = 'And "tail" text.'

child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
child_with_entity_ref.text = 'This & that'

<?xml version="1.0" encoding="UTF-8"?>
<data>
    <shop>
        <item count="668" price="2" bundleId="sg.candy2.gold.01"/>
        <item count="1750" price="5" bundleId="sg.candy2.gold.02"/>
        <item count="4000" price="10" bundleId="sg.candy2.gold.03"/>
        <item count="11250" price="25" bundleId="sg.candy2.gold.04"/>
        <item count="25000" price="50" bundleId="sg.candy2.gold.05"/>
        <item count="60000" price="99.99" bundleId="sg.candy2.gold.06"/>
    </shop>
</data>


{"packages": [{"id": "1", "BundleId": "sg.candy2.gold.01", "Price": 2.0, "Type": "Money", "Namekey": "gui_pacakge1_key_locale", "Count": 668}, {"id": "2", "BundleId": "sg.candy2.gold.02", "Price": 5.0, "Type": "Money", "Namekey": "gui_pacakge2_key_locale", "Count": 1750}, {"id": "3", "BundleId": "sg.candy2.gold.03", "Price": 10.0, "Type": "Money", "Namekey": "gui_pacakge3_key_locale", "Count": 4000}, {"id": "4", "BundleId": "sg.candy2.gold.04", "Price": 25.0, "Type": "Money", "Namekey": "gui_pacakge4_key_locale", "Count": 11250}, {"id": "5", "BundleId": "sg.candy2.gold.05", "Price": 50.0, "Type": "Money", "Namekey": "gui_pacakge5_key_locale", "Count": 25000}, {"id": "6", "BundleId": "sg.candy2.gold.06", "Price": 100.0, "Type": "Money", "Namekey": "gui_pacakge6_key_locale", "Count": 60000}], "ShopIds": [1, 2, 3, 4, 5, 6]}
"""
def GetJson(path : str) -> {}:
    file = open(path)
    json_data = json.load(file)
    return json_data



def Main(out_name : str, path : str) -> None:
    top  = Element("data")
    shops = SubElement(top,"shop")
    #tree = ET(top_data)
    #top_shop = SubElement(top_data, "shop")
    json_data = GetJson(path)
    json_packages = json_data.get("packages")
    for _ in json_packages:
        item = SubElement(shops,"item", {
            'count':str(_.get("Count")),
            'price':str(_.get("Price")),
            'bundleId':str(_.get("BundleId"))
        })

    doc = ElementTree(top)
    outFile = open(name, 'wb')
    doc.write(outFile)

name = sys.argv[1]
path = sys.argv[2]
Main(name, path)
exit(0)


