#!/usr/bin/python2.7
import shapely, string 
from shapely.geometry import Polygon, Point
from lxml import etree
from os import path
from optparse import OptionParser

import sys

XHTML_NAMESPACE = "http://earth.google.com/kml/2.2"
XHTML = "{%s}" % XHTML_NAMESPACE
NSMAP = {None : XHTML_NAMESPACE}

def poly_list(list_string):
  coord_list = []
  for point in list_string.split(" "):
    coords = point.split(",")
    #print "(" + coords[1] + "," + coords[0] + ")"
    coord_list.append((float(coords[1]),float(coords[0]))) # Google KML has order of (Long, Lat), so converting to (Lat, Long)
    #print coord_list
  #print "Coordinate List is " + str(type(coord_list))
  #for tup in coord_list:
  #  print "Coord is " + str(type(tup))
  #Polygon(coord_list)
  return coord_list

def sev_index(cat_type):
  return {
    'General Thunder' : 0,
    'Marginal Risk' : 1,
    'Slight Risk' : 2,
    'Enhanced Risk' : 3,
    'Moderate Risk' : 4,
    'High Risk' : 5
  }.get(cat_type, -1)

def sev_index_str(cat_index):
  return {
    0 : 'General Thunderstorm',
    1 : 'Marginal',
    2 : 'Slight',
    3 : 'Enhanced',
    4 : 'Moderate',
    5 : 'High'
  }.get(cat_index, 'None')

def sev_index_str_short(cat_index):
  return {
    0 : 'TSTM',
    1 : 'MRGL',
    2 : 'SLGT',
    3 : 'ENH',
    4 : 'MDT',
    5 : 'HIGH'
  }.get(cat_index, 'NONE')

def polygon_parser(poly_elm):
  outer = []
  inner = []
  for child in poly_elm:
    if(child.tag == XHTML + "outerBoundaryIs"):
     outer = poly_list(child.find(".//" + XHTML + "coordinates").text)
    if(child.tag == XHTML + "innerBoundaryIs"):
     inner.append(poly_list(child.find(".//" + XHTML + "coordinates").text))
  #print "inner = " + str(len(inner))
  #print "Outer " + str(outer)
  #for inner_list in inner:
  #  print "Inner: " + str(inner_list)
  return Polygon(outer, inner)

loc = Point(35.4432945,-97.5958710)
parser = etree.XMLParser(ns_clean=True)
cat_list = ("http://www.spc.noaa.gov/products/outlook/day1otlk_cat.kml","http://www.spc.noaa.gov/products/outlook/day2otlk_cat.kml","http://www.spc.noaa.gov/products/outlook/day3otlk_cat.kml")

#creating flags
optParser = OptionParser()
optParser.add_option("-s", "--short", "--conky", dest="short", action="store_true", help="Display shorthand output instead", default=False)
optParser.add_option("-l", "--legacy", dest="legacy", action="store_true", help="Interprets file as pre-2014 change to Risk Areas", default=False)
optParser.add_option("-p", "--point", "--coord", dest="location", metavar="LAT,LONG", help="Specifiy currently location in Latitude & Longitude")
(options, args) = optParser.parse_args()

if options.location is not None:
  coords = options.location.split(",")
  loc = Point(float(coords[0]),float(coords[1]));

for day in xrange(3):
  #day_cat = etree.parse("examples/day1otlk_cat.kml", parser)
  day_cat = etree.parse(cat_list[day], parser)
  legacy = options.legacy #for Interpting older KML (as tests) - didn't have Marginal nor Enhanced
  risk = -1
  root = day_cat.getroot()
  risk_areas = root.findall(".//" + XHTML + "Placemark")
  poly_risk_areas = [[],[],[],[],[],[]]
# 0 -> TimeSpan
# 1 -> name
# 2 -> Style
# 3 -> ExtendedData
# 4 -> Polygon
  for risk_area in risk_areas:
    poly_risk_areas[sev_index(risk_area[1].text)].append(polygon_parser(risk_area[4]))
  for x in xrange(6):
    if(len(poly_risk_areas[x]) == 0 and not(legacy and (x == 1 or x == 3))):
      break
    else:
      for risk_poly in poly_risk_areas[x]:
        #print "Testing in risk area " + sev_index_str(x)
        if(loc.within(risk_poly)):
          risk = x
  if(options.short):
    if(risk == -1):
      print "Day " + str(day+1) + ": NONE"
    else:
      print "Day " + str(day+1) + ": " + sev_index_str_short(risk)
  else:
    if(risk == -1):
      print "Day " + str(day+1) + ": not in risk area"
    else:
      print "Day " + str(day+1) + ": within " + sev_index_str(risk) + " risk area" 
#  for child in risk_area:
#    if(child.tag == XHTML + "name"):
#    print child.text + " -> " + str(sev_index(child.text))
#    elif(child.tag == XHTML + "Polygon"):
#    polygon_parser(child)

