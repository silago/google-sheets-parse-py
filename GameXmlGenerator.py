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
    doc.write(outFile, encoding='UTF-8', xml_declaration=True)

name = sys.argv[1]
path = sys.argv[2]
Main(name, path)
exit(0)


