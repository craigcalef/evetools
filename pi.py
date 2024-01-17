import csv, itertools, locale, sys, math
from pprint import pprint, pformat
from util import pairs
from p0 import pc, basemats, p1, p2, p1p0, spairs, schematics
from prices import p1prices, p2prices, prices
from evecentral import MarketData
from stores import mats
from blueprints import blueprints, types
from db import *

ME = 0.90

schematics += blueprints.items()

floormat = p1

marketprices = MarketData()

def formatingredient(ingredient, mult=1):
  price = marketprices.getbyname(ingredient[0])['buy']['max']
  #return "%g %s (%s)" % (ingredient[1] * mult, ingredient[0], "${0:,.0f}".format(ingredient[1] * mult * price, grouping=True))
  return "{0:,} {1} ($ {2:,.0f})".format(ingredient[1] * mult, ingredient[0], ingredient[1] * mult * price)

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

  # HACK
  if 'R.A.M.' in mat:
    return
  # HACK

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
    #submats = reducemat(ingredient[0], icnt)
    submats = reducemat(ingredient[0], math.ceil(icnt * ME))
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
    #return prices[mat]
    return marketprices.getbyname(mat)['buy']['max']
 
def summarizecommodities(cl):
  clcomb = combineboms([reducemat(*i) for i in cl]).items()
  clcomb.sort(key=lambda x: x[1])
  costs = 0
  for i in clcomb:
    #print formatingredient(i), "%g" % float(mats[i[0]]) / float(i[1])
    print formatingredient(i), float(mats[i[0]]) / float(i[1])
    #print formatingredient(i)
    costs += baseprice(i[0]) * i[1]
  print "Total cost: %f" % costs
  
def analyzeitemprofit(itemname, f):
  reqs = reducemat(itemname, 1)
  if not reqs:
    print "Item not reducable:", itemname
    return
  #pprint.pprint(reqs)
  costs = 0
  needs = []
  for i in reqs.items():
    nvalue = float(mats[i[0]]) / float(i[1]) 
    if not 'R.A.M.' in i[0]:
      needs.append(nvalue)
    print i[0], float(mats[i[0]]), float(i[1]), nvalue
    costs += baseprice(i[0]) * i[1]
 
  potential = min(needs)
  #pprint.pprint(marketprices.getbyname(itemname))
  sell = marketprices.getbyname(itemname)['sell']['avg']
  #pprint.pprint(sell)
  #print itemname, costs, sell, sell - costs, potential, (sell - costs) * potential
  summary =  "%s,%f,%f,%f,%f,%f" % ( itemname, costs, sell, sell - costs, potential, (sell - costs) * potential )
  print summary
  f.write(summary + "\n")
  #print itemname, costs, sell, sell - costs

#  clsch = []
#  for scheg in itertools.chain([recursemat(t[0]) for t in cl]):
#    for sche in scheg:
#      pprint(sche)
#      if not sche in clsch:
#        clsch.append(sche)
#  for s in clsch:
#    print formatschematic(s)

if __name__ == '__main__':
  summarizecommodities([(sys.argv[1], 1)])
  sys.exit(0)
  ibg = itemsByGroups(marketSubGroupsByName(sys.argv[1]))
  pprint.pprint(ibg)
  if len(ibg) > 0:
    if len(sys.argv) > 2:
      f = open(sys.argv[2], "w")
    else:
      f = sys.stdout
    for item in ibg:
      analyzeitemprofit(item, f)
    f.flush()
    f.close()
#summarizecommodities([(u'Proteus Defensive - Augmented Plating', 1)])
#summarizecommodities([(u'Incursus', 1)])
#summarizecommodities([(u'Proteus', 1)])
#summarizecommodities([(u'Proteus', 1)])
#summarizecommodities([(u'Capital Armor Plates', 1)])
#summarizecommodities([(u'Mobile Depot', 1)])
#pprint(reducemat(u'Proteus Defensive - Augmented Plating', 1))
#pprint(reducemat(u'Proteus Defensive - Augmented Plating', 1))
#pprint([recursemat('Wetware Mainframe')])
