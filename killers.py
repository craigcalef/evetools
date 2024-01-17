import json

d = json.loads(open('zkillboard.json').read())

for v in d:
  for a in v['attackers']:
    if not a['corporationName'] == 'Sleeper Slumber Party' and not a['corporationName'] == 'Jump Drive Appreciation Society':
      print a['corporationName']
