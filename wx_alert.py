#!/usr/bin/python3
import string
from os import path
from optparse import OptionParser
import feedparser
import dateutil.parser as dateparser
import datetime

def shorthand(alert_type):
  return {
    'Air Stagnation Advisory' : 'Air Stag Adv',
    'Dense Fog Advisory' : 'Dense Fog Adv',
    'Wind Advisory' : 'Wind Adv',
    'Red Flag Warning' : 'Red Flag Warn'
  }.get(alert_type, "NEW")

#creating flags
optParser = OptionParser()
optParser.add_option("-s", "--short", "--conky", dest="short", action="store_true", help="Display shorthand output instead", default=False)
optParser.add_option("-l", "--loc", dest="location", metavar="XXX###", help="Specifiy currently location Zone")
(options, args) = optParser.parse_args()

if(options.location is not None):
  loc = options.location
else:
  loc = 'OKZ029'
url = 'http://alerts.weather.gov/cap/wwaatmget.php?x=' + loc
feed = feedparser.parse(url)
if feed['entries'][0]['title'] == "There are no active watches, warnings or advisories":
  print("No active alerts.")
else:
  for alert in feed['entries']:
    if(options.short):
      alert_type = shorthand(alert['cap_event'])
    else:
      alert_type = alert['cap_event']
    alert_end = dateparser.parse(alert['cap_expires'])
    alert_start = dateparser.parse(alert['cap_effective'])
    if (alert_end.day > datetime.datetime.now(alert_end.tzinfo).day):
      alert_string = alert_end.strftime(" until %a %I:%M %p")
    else:
      alert_string = alert_end.strftime(" until %I:%M %p")
    if (alert_start > datetime.datetime.now(alert_start.tzinfo)):
      if (alert_start.day > datetime.datetime.now(alert_start.tzinfo).day):
        alert_string = alert_start.strftime("From %a %I:%M %p ") + alert_string
      else:
        alert_string = alert_start.strftime("From %I:%M %p ") + alert_string
    print(alert_type + alert_string)
