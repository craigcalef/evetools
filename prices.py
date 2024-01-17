import json, os, pprint, itertools
from collections import defaultdict
price_key = 'buy_price'

def load_prices(filename):
  return dict( [ (i['name'], float(i[price_key].replace(',',''))) for i in json.loads(open(filename).read())['items'] ] )

p0prices = load_prices('p0prices.json')
p1prices = load_prices('p1prices.json')
p2prices = load_prices('p2prices.json')
p3prices = load_prices('p3prices.json')
p4prices = load_prices('p4prices.json')

pricesl = []
prices = defaultdict(float)

for f in os.listdir('.'):
  if f.endswith('prices.json'):
    p = load_prices(f)
    pricesl.append(p)
    prices.update(p)

#prices = defaultdict(float, [(x[0], float(x[1])) for x in list(itertools.chain(*pricesl))])

vol = [0.01, 0.38, 1.5, 6, 100]

def price_breakdown():
  a = zip(vol, pricesl)
  pm = [] 
  for x in a:
    for i in x[1].items():
      pm.append((i[0], float(i[1]) / x[0]))

  pm.sort(key=lambda x: x[1])
  for i in pm:
    print i[0], i[1]


