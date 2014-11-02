#!/usr/bin/python2.7
import shapely, string 
from shapely.geometry import Polygon, Point
from lxml import etree
from os import path

XHTML_NAMESPACE = "http://earth.google.com/kml/2.2"
XHTML = "{%s}" % XHTML_NAMESPACE
NSMAP = {None : XHTML_NAMESPACE}

def sev_index(cat_type):
  return {
    'General Thunder' : 0,
    'Marginal Risk' : 1,
    'Slight Risk' : 2,
    'Enhanced Risk' : 3,
    'Moderate Risk' : 4,
    'High Risk' : 5,
  }.get(cat_type, -1)

def polygon_parser(poly_elm):
  return 0

parser = etree.XMLParser(ns_clean=True)
day_1_cat = etree.parse("examples/day2otlk_cat.kml", parser)
root = day_1_cat.getroot()
risk_areas = root.findall(".//" + XHTML + "Placemark")
for risk_area in risk_areas:
  for child in risk_area:
    if(child.tag == XHTML + "name"):
      print child.text + " -> " + str(sev_index(child.text))

