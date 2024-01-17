import csv
from collections import defaultdict
from pprint import pprint

mats = defaultdict(int)

line = []
r = csv.reader(open('s.csv'), dialect='excel-tab')
for l in r:
  try:
    mats[l[0]] += int(l[1].replace(',', ''))
  except:
    pass

