#!/usr/bin/python2.7
import string
from lxml import etree
from os import path
from optparse import OptionParser

loc = 'OKZ025'
url = 'http://alerts.weather.gov/cap/wwaatmget.php?x=' + loc
alert_tree = etree.parse(url).getroot();

