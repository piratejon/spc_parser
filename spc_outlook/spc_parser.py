#/bin/python
"""
Shapely - for making pylgons from lat/long coordinates
re - regular expressions
"""
import shapely, re, string
from shapely.geometry import Polygon, Point

def return_category(category, text):
  regex_array = {
    'split' : re.compile('\.\.\..*?&&', re.DOTALL),
    'categorical' : re.compile('CATEGORICAL'),
    'tornado' : re.compile('TORNADO'),
    'hail' : re.compile('HAIL'),
    'wind' : re.compile('WIND'),
    'severe' : re.compile('ANY SEVERE')
  }
  split_result = regex_array['split'].findall(text)
  if split_result:
    for result in split_result:
      if regex_array[category].search(result):
        return result
  else:
    return False
def return_subcategory(category, text):
  regex_array = {
    # General Risk,
    'high' : re.compile('(HIGH   [(\d{8})( |\s       )]*\d{8})'),
    'moderate' : re.compile('(MDT    [(\d{8})( |\s       )]*\d{8})'),
    'slight' : re.compile('(SLGT   [(\d{8})( |\s       )]*\d{8})'),
    'general' : re.compile('(TSTM   [(\d{8})( |\s       )]*\d{8})'),
    2 : re.compile('(0.02   [(\d{8})( |\s       )]*\d{8})'), 
    5 : re.compile('(0.05   [(\d{8})( |\s       )]*\d{8})'), 
    10 : re.compile('(0.10   [(\d{8})( |\s       )]*\d{8})'), 
    15 : re.compile('(0.15   [(\d{8})( |\s       )]*\d{8})'),
    30 : re.compile('(0.30   [(\d{8})( |\s       )]*\d{8})'),
    45 : re.compile('(0.45   [(\d{8})( |\s       )]*\d{8})'),
    60 : re.compile('(0.60   [(\d{8})( |\s       )]*\d{8})'),
    "SIGN" : re.compile('(SIGN   [(\d{8})( |\s       )]*\d{8})') 
  }
  if regex_array[category]:
    print "FAIL"
  if(category == "high" or category == "moderate" or category == "slight" or category == "general" or category == 2):
    result = regex_array[category].findall(text)
    return result
  else:
    print "NOT MADE YET or FAIL"


def toPolygon(text):
  coordinates = text.split()
  coordinates = coordinates[1:]
  coord_list = []
  for coord in coordinates:
    lat = int(coord[:4])/100.0
    lon = -int(coord[4:])/100.0
    if lon > -50:
      lon = lon-100
    if (lon == -99.99 and lat == 99.99):
      continue
    coord_list.append((lat,lon))
  return Polygon(coord_list)

def in_cat_risk_area(polygons_list):
  return_string = "Not in a risk area"
  total = len(polygons_list)
  while len(polygons_list) > 0:
    polygon_list = polygons_list.pop()
    for i, polygon in enumerate(polygon_list):
      if (not(polygon.contains(chicago)) and (i  < len(polygon_list))):
        return total - len(polygons_list) - 1
  return False
manor = Point(35.209205,-97.451605)
chicago = Point(41.8819,-87.6278) # for day 1 sign outlook
#importing the polygon list and concatinating into one long string for regex parsing
day_1_risk = open('high_risk_day_1.txt', 'r') # test file with all risk categories
risk_list = day_1_risk.readlines()
risk_text = "".join(risk_list)
"""
lists of poygons
"""
high_risk_polygon = []
mod_risk_polygon = []
slight_risk_polygon = []
general_risk_polygon = []

categorical_text = return_category("categorical",risk_text)
if categorical_text:
  high_text = return_subcategory("high", categorical_text)
  if high_text:
    for result in high_text:
      high_risk_polygon.append(toPolygon(result))
  mod_text = return_subcategory("moderate", categorical_text)
  if mod_text:
    for result in mod_text:
      mod_risk_polygon.append(toPolygon(result))
  slight_text = return_subcategory("slight", categorical_text)
  if slight_text:
    for result in slight_text:
      slight_risk_polygon.append(toPolygon(result))
  general_text = return_subcategory("general", categorical_text)
  if general_text:
    for result in general_text:
      general_risk_polygon.append(toPolygon(result))
else:
  print "FAIL"

risk_area = in_cat_risk_area([high_risk_polygon, mod_risk_polygon, slight_risk_polygon, general_risk_polygon])

'''
Probablity Polygons
'''

tornado_risk_area = return_category("tornado",risk_text)
print "Tornado risk area: " + str(tornado_risk_area)
if tornado_risk_area:
  two_perc_area = return_subcategory(2, tornado_risk_area)
  print two_perc_area
return_subcategory(4,"test")
