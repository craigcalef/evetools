from api import *

chars = getCharacters()
pprint(chars)
for char in chars:
    print char['name']
    planets = getPlanets(char['characterid'])
    for planet in planets:
      print "\t", planet['planetname']
      pins = getPins(char['characterid'], planet['planetid'])
      for pin in pins:
        if 'Extractor' in pin['typename']:
          print "\t\t", pin['installtime'], pin['expirytime'], pin['quantitypercycle']
      
