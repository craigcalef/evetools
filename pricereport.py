from evecentral import MarketData
import csv

marketprices = MarketData()

modprices = { 
'Fullerite-C320': ('buy', 0.90),
'Fullerite-C540': ('buy', 0.90),
'Fullerite-C70': ('buy', 0.90),
'Fullerite-C50': ('buy', 0.90),
'Fullerite-C32': ('buy', 0.90),
'Fullerite-C60': ('buy', 0.0),
'Fullerite-C28': ('buy', 0.0),
'Fullerite-C84': ('sell', 1.1),
'Fullerite-C72': ('sell', 1.1),
}

l = []

try:
  while True:
    l.append(raw_input())
except:
  pass

c = csv.reader(l, dialect='excel-tab') 

tt = 0
print "item \t quantity \t orig $ \t order \t perc. \t mod'd \t subtotal"
for r in c:
  p = marketprices.getbyname(r[0])

  if r[0] in modprices.keys():
    mod = modprices[r[0]]
  else:
    mod = ('buy', 1.0)

  if mod[0] == 'buy':
    op = p[mod[0]]['max']
  else:
    op = p[mod[0]]['min']
  
  #a = p
  #print a['buy']['min'], a['buy']['max'], a['buy']['avg'], '\n', a['sell']['min'], a['sell']['max'], a['sell']['avg'] 
   
  mp = op * mod[1]  # modified price
  # I know there is a more proper way to parse region specific commas
  totes = mp * int(r[1].replace(',', ''))
  print "{}\t{}\t{}\t{}\t{}\t{}".format(r[0],r[1], op, mod[0], mod[1], mp, totes)
  tt += totes

print "Total\t{}".format(tt)


