from util import pairs
import csv, sqlite3, yaml

pc = [['Bacteria', '20', 'Microorganisms', '3000'],
 ['Biofuels', '20', 'Carbon Compounds', '3000'],
 ['Biomass', '20', 'Planktic Colonies', '3000'],
 ['Chiral Structures', '20', 'Non-CS Crystals', '3000'],
 ['Electrolytes', '20', 'Ionic Solutions', '3000'],
 ['Industrial Fibers', '20', 'Autotrophs', '3000'],
 ['Oxidizing Compound', '20', 'Reactive Gas', '3000'],
 ['Oxygen', '20', 'Noble Gas', '3000'],
 ['Plasmoids', '20', 'Suspended Plasma', '3000'],
 ['Precious Metals', '20', 'Noble Metals', '3000'],
 ['Proteins', '20', 'Complex Organisms', '3000'],
 ['Reactive Metals', '20', 'Base Metals', '3000'],
 ['Silicon', '20', 'Felsic Magma', '3000'],
 ['Toxic Metals', '20', 'Heavy Metals', '3000'],
 ['Water', '20', 'Aqueous Liquids', '3000']]

p3 = ['Broadcast Node', 'Integrity Response Drones', 'Nano-Factory', 'Organic Mortar Applicators',
      'Recursive Computing Module', 'Self-Harmonizing Power Core', 'Sterile Conduits', 'Wetware Mainframe']

basemats = [i[2] for i in pc]
p1 = [i[0] for i in pc]
p1p0 = {}
for i in pc:
  p1p0[i[0]] = i[2]
m = [list(pairs(l)) for l in pc]
#pprint.pprint(m)

# Load schematics. Probably would be better refactored into another file/function
r = csv.reader(open('schematics.csv'))
sraw = [l for l in r]
for l in sraw:
  l.reverse()

p2csv = csv.reader(open('p2.csv'))
p2 = [l[0] for l in p2csv]

spairs = []
for l in sraw:
  spairs.append( ((l[0], l[1]), [pair for pair in pairs(l[2:])]))
schematics = []
for l in spairs:
  a = ((l[0][0], int(l[0][1])), [(ll[0], int(ll[1])) for ll in l[1]])
  #pprint(a)
  schematics.append(a)

