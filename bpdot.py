import csv, itertools, locale, sys
from pprint import pprint, pformat
from util import pairs
from p0 import pc, basemats, p1, p2, p1p0, spairs, schematics
from prices import p1prices, p2prices, prices
from stores import mats
from blueprints import blueprints, types

schematics += blueprints.items()

floormat = p1

def formatingredient(ingredient, mult=1):
  return "%g %s (%s)" % (ingredient[1] * mult, ingredient[0], "${0:,.0f}".format(ingredient[1] * mult * prices[ingredient[0]], grouping=True))

def formatschematic(schematic, mult=1):
  return "%s <= %s" % (formatingredient(schematic[0], mult), ", ".join([formatingredient(i,mult) for i in schematic[1]]))

def recursemat(mat):
  """ Generate schematics recursively from a material. """
  #if mat in basemats:
  if mat in floormat:
    return

  for s in schematics:
    if s[0][0] == mat:
      yield s
      for ingredient in s[1]:
        for ss in recursemat(ingredient[0]):
          yield ss

def reducemat(mat, cnt):
  """ Reduce the ingredients needed for a specified number of planetary
  commodities, recursing to its base extraction materials """
  sch = None
  for s in schematics:
    if s[0][0] == mat:
      sch = s
  if not sch:
    #raise Exception("Material not found: %s" % mat)
    return
  
  # Normalize reduced material count to a fraction of the recipe output
  bm = float(cnt) / float(sch[0][1]) 
  ret = {}
  print formatschematic(sch, bm)
  for ingredient in sch[1]:
    icnt = ingredient[1] * bm
    ret[ingredient[0]] = icnt
    submats = reducemat(ingredient[0], icnt)
    if not submats is None:
      for smk in submats.keys():
        ret[smk] = ret.get(smk, 0) + submats[smk]
  return ret

def combineboms(boms):
  """ There is probably already a function that does this.
  Combine two dictionaries with default values of 0 """
  ret = {}
  for bom in boms:
    for mk in bom.keys():
      ret[mk] = ret.get(mk, 0) + bom[mk]
  return ret
 
def baseprice(mat):
  sch = None
  for s in schematics:
    if s[0][0] == mat:
      sch = s
  if sch:
    return 0
  else:
    return prices[mat]
 
def dotblueprint(cl):
  print "digraph {"
  for i in recursemat(cl):
    for ii in i[1]:
      print '"{}" -> "{}"'.format(i[0][0], ii[0])
  print "}"
  
#  clsch = []
#  for scheg in itertools.chain([recursemat(t[0]) for t in cl]):
#    for sche in scheg:
#      pprint(sche)
#      if not sche in clsch:
#        clsch.append(sche)
#  for s in clsch:
#    print formatschematic(s)

if __name__ == '__main__':
  dotblueprint(sys.argv[1])

