import json, os, pprint, itertools, traceback, requests, time, pprint, itertools, uuid, csv
from collections import defaultdict

PRICE_CACHE_DIR = "pricecache"
HINTCACHE_AGE_LIMIT = 24 * 60 * 60 # 1 Day

typescsv = csv.reader(open('types.csv'))
typeslist = [(l[1], int(l[0])) for l in typescsv]
typesnameid = dict(typeslist)

def parseevecentraljson(jsontxt):
  buy = {}
  sell = {}
  all = {}
  try:
    d = json.loads(jsontxt)
    for i in d:
      buy[i['buy']['forQuery']['types'][0]] = i['buy']
      sell[i['sell']['forQuery']['types'][0]] = i['sell']
      all[i['all']['forQuery']['types'][0]] = i['all']
  except:
    traceback.print_exc()
    print jsontxt
  return buy, sell, all
    
def evecentralmarketstats(typeids):
  return requests.get("http://api.eve-central.com/api/marketstat/json", params={"typeid": ["%d" % i for i in typeids], 'usesystem': '30000142'}).text
  #return requests.get("http://api.eve-central.com/api/marketstat/json", params={"typeid": ["%d" % i for i in typeids] }).text

class MarketData:
  def __init__(self):
    self.hints = set()
    self.buy = {}
    self.sell = {}
    self.all = {}

    # Look for a set of 'hints' we use to run an initial cache-refresh
    #try:
    #  f = open(os.path.join(PRICE_CACHE_DIR, 'typehints.txt'))
    #  for l in f.readlines():
    #    t = int(l.strip())
    #    self.hints.append(t)
    #except:
    #  print "Error loading cache hints."
    #  traceback.print_exc()

    for f in os.listdir(PRICE_CACHE_DIR):
      if f.endswith('.json'):
        cache_file = os.path.join(PRICE_CACHE_DIR, f)
        if time.time() - os.stat(cache_file).st_mtime < HINTCACHE_AGE_LIMIT:
          jsontxt = open(cache_file).read()
          buy, sell, all = parseevecentraljson(jsontxt)
          self.buy.update(buy)
          self.sell.update(sell)
          self.all.update(all)
        else:
          # If the cache is old, grab the keys for a cache-update hint then delete
          jsontxt = open(cache_file).read()
          buy, sell, all = parseevecentraljson(jsontxt)
          for i in itertools.chain(buy.keys(), sell.keys(), all.keys()):
            self.hints.add(int(i)) 
          os.remove(cache_file) 

    if len(self.hints) > 0:
      self.gettypes(self.hints)
  
  def getbyname(self, name):
    return self.get(typesnameid[name])

  def get(self, type):
    rbuy, rsell, rall = self.gettypes([type])
    return {"buy": rbuy[type], "sell": rsell[type], "all": rall[type]}

  def gettypes(self, types):
    rbuy = {}
    rsell = {}
    rall = {}
 
    fetch = set()
    for type in types:
      if type in self.buy.keys():
        rbuy[type] = self.buy[type]
        rsell[type] = self.sell[type]
        rall[type] = self.all[type]
      else:
        #print "Type: ", type
        fetch.add(type)

    # if we found all we were asked for, return them.
    if len(fetch) == 0:
      return rbuy, rsell, rall

    # if requested price data was requested by not found, fetch it, cache it, and return it
    # in addition to those that were found.
    jsontxt = evecentralmarketstats(list(fetch))
    f = open(os.path.join(PRICE_CACHE_DIR, "%s.json" % uuid.uuid4()), 'w')
    f.write(jsontxt)
    f.flush()
    f.close()
    fbuy, fsell, fall = parseevecentraljson(jsontxt)
    rbuy.update(fbuy); self.buy.update(fbuy)
    rsell.update(fsell); self.sell.update(fsell)
    rall.update(fall); self.all.update(fall)
    return rbuy, rsell, rall

