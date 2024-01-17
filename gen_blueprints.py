# Generate simple data formats for typeID data and blueprints

import sqlite3, pprint, yaml, json, traceback, pickle

c = sqlite3.connect('eve.db')
types = {}

f = open('types.csv', 'w')
for r in c.execute("select * from invTypes"):
  types[r[0]] = r[1]
  f.write("%d,%s\n" % (r[0], r[1].encode('UTF-8')))
f.flush()
f.close()

pprint.pprint(types)

bp = yaml.load(open('blueprints.yaml'))

blueprints = {}

for tid in bp.keys():
  try:
    mats = []
    for m in bp[tid]['activities']['manufacturing']['materials']:
      mats.append((types[m['typeID']], m['quantity']))
      blueprints[(types[bp[tid]['activities']['manufacturing']['products'][0]['typeID']], bp[tid]['activities']['manufacturing']['products'][0]['quantity'])] = mats
  except:
    print "Error:", tid
    traceback.print_exc()

f = open('blueprints.pickle', 'w')
f.write(pickle.dumps(blueprints))
f.flush()
f.close()

