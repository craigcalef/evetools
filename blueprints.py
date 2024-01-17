import sqlite3, pprint, yaml, json, traceback, pickle, sys

c = sqlite3.connect('eve.db')
types = {}

for r in c.execute("select * from invTypes"):
  types[r[0]] = r[1]

blueprints = pickle.loads(open('blueprints.pickle').read())

if __name__ == '__main__':
  for k in blueprints.keys():
    for b in blueprints[k]:
      if b[0] == sys.argv[1]:
        print k[0]
