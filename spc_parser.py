import shapely, string, pykml
from shapely.geometry import Polygon, Point
#from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree
from os import path
import xml.etree.ElementTree as ET

day_1_cat_file = path.join("examples/day1otlk_cat.kml")

with open(day_1_cat_file) as day_1_cat_open:
  day_1_cat = parser.parse(day_1_cat_open)
root = day_1_cat.getroot()
#print etree.iselement(root.Document.Folder.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates)
#print etree.tostring(etree.ElementTree(root),pretty_print=True)
child1 = root[1]
print(child1.tag)
