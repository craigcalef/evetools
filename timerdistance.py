import json, requests, sys, shelve, datetime, dateutil.parser

eventTypes = {
  1: "TCU",
  2: "IHub",
  3: "Station",
  4: "Freeport"
}

timer_endpoint = 'https://public-crest.eveonline.com/sovereignty/campaigns/'

default_start = 'U-HVIX'
if len(sys.argv) > 1:
  startpoint = sys.argv[1]
else:
  startpoint = default_start

timers = json.loads(requests.get(timer_endpoint).text)

distancecache = shelve.open('distancecache.db', 'c')

tb = []

jo = {}
jo['items'] = []

for i in timers['items']:
  l = i['sourceSolarsystem']['name']
  try:
    d = distancecache['%s:%s' % (startpoint, l)]
  except:
    r = requests.get('http://api.eve-central.com/api/route/from/%s/to/%s' % (startpoint, l)).text
    dj = json.loads(r)
    d = len(dj)
    distancecache['%s:%s' % (startpoint, l)] = d

  if 'defender' in i.keys():
    defender = i['defender']['defender']['name']
  else:
    defender = 'None'
  eventtimer = str(dateutil.parser.parse(i['startTime']) - datetime.datetime.now()).replace(',', '')
  
  tb.append((l, d, defender, eventtimer, eventTypes[i['eventType']]))
  jo['items'].append( {
     'startTime': i['startTime'],
     'sourceSolarsystemName': i['sourceSolarsystem']['name'],
     'jumps': d,
     'eventType': i['eventType'],
     'owner': defender } )

tb.sort(key=lambda x: x[1])

#for i in tb:
#  print "{},{},{},{},{}".format(*i)
    
f = open('campaigns.json', 'w')
f.write(json.dumps(jo))
f.flush()
f.close()

distancecache.close()
