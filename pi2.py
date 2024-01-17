import csv, itertools
from pprint import pprint, pformat
from util import pairs
from p0 import pc, basemats, p1, p1p0

m = [list(pairs(l)) for l in pc]
#pprint.pprint(m)

# Load schematics. Probably would be better refactored into another file/function
r = csv.reader(open('schematics.csv'))
sraw = [l for l in r]
for l in sraw:
  l.reverse()

spairs = []
for l in sraw:
  spairs.append( ((l[0], l[1]), [pair for pair in pairs(l[2:])]))
schematics = []
for l in spairs:
  a = ((l[0][0], int(l[0][1])), [(ll[0], int(ll[1])) for ll in l[1]])
  #pprint(a)
  schematics.append(a)

floormat = p1

def formatingredient(ingredient, mult=1):
  if ingredient[0] in p1:
    i = "%s/%s" % (ingredient[0], p1p0[ingredient[0]])
  else:
    i = ingredient[0] 
  return "%g %s" % (ingredient[1] * mult, ingredient[0])

def formatschematic(schematic, mult=1):
  return "%s <= %s" % (formatingredient(schematic[0], mult), ", ".join([formatingredient(i,mult) for i in schematic[1]]))

def recursemat(mat):
  """ Generate schematics recursively from a material. """
  #if mat in basemats:
  if mat in p1:
    return

  for s in schematics:
    if s[0][0] == floormat:
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
    raise Exception("Material not found: %s" % mat)
  
  # Normalize reduced material count to a fraction of the recipe output
  bm = float(cnt) / float(sch[0][1]) 
  ret = {}
  print formatschematic(sch, bm)
  for ingredient in sch[1]:
    icnt = ingredient[1] * bm
    if not ingredient[0] in floormat:
      submats = reducemat(ingredient[0], icnt)
      for smk in submats.keys():
        ret[smk] = ret.get(smk, 0) + submats[smk]
    else:
      ret[ingredient[0]] = icnt
  return ret

def combineboms(boms):
  ret = {}
  for bom in boms:
    for mk in bom.keys():
      ret[mk] = ret.get(mk, 0) + bom[mk]
  return ret
 
mtu = [("Organic Mortar Applicators", 2),
       ("Ukomi Superconductors", 2),
       ("Wetware Mainframe", 1)]
 
p3 = ['Broadcast Node', 'Integrity Response Drones', 'Nano-Factory', 'Organic Mortar Applicators',
      'Recursive Computing Module', 'Self-Harmonizing Power Core', 'Sterile Conduits', 'Wetware Mainframe']

def summarizecommodities(cl):
  clcomb = combineboms([reducemat(*i) for i in cl]).items()
  clcomb.sort(key=lambda x: x[1])
  #p3ingred = reducemat(p3mat, 1)
  #pprint(p3ingred)
  #totp1 = 0
  #for i in p3ingred:
  #  totp1 = totp1 + i[1]
  totp1 = sum([l[1] for l in clcomb])
  for i in clcomb:
    print formatingredient(i), "%g" % (i[1] / (totp1 / 15))
  print "Total p1 mats: %g" % totp1
  
#  clsch = []
#  for scheg in itertools.chain([recursemat(t[0]) for t in cl]):
#    for sche in scheg:
#      pprint(sche)
#      if not sche in clsch:
#        clsch.append(sche)
#  for s in clsch:
#    print formatschematic(s)

summarizecommodities(mtu)
#pprint([recursemat('Wetware Mainframe')])
