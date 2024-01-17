from credentials import *
import BeautifulSoup, requests
requests.packages.urllib3.disable_warnings()
from pprint import pprint

def EVEAPIException(BaseException):
  pass
#  def __init__(self, msg, code, keyid, vcode):
#    super(EVEAPIException, self).__init__(msg)
#    self.msg = msg
#    self.code = code
#    self.keyid = keyid
#    self.vcode = vcode

def eveApiRequest(endpoint, **kwparams):
  p = {'keyID':KEYID, 'vCode': VCODE}
  p.update(kwparams)
  return eveApiSendRequest(endpoint, p)

def eveCorpApiRequest(endpoint, kwparams={}):
  p = {'keyID':CORPKEYID, 'vCode': CORPVCODE}
  p.update(kwparams)
  return eveApiSendRequest("https://api.eveonline.com"+endpoint, p)

def eveApiSendRequest(endpoint, p):
  xml = requests.get(endpoint, params=p)
  soup = BeautifulSoup.BeautifulSoup(xml.text)
  e = soup.findAll('error')
  if e:
    raise Exception(e['text'])
  return soup

def eveApi(endpshort, kwparams):
  endpoint = 'https://api.eveonline.com/%s' % endpshort
  #p = {'keyID':KEYID, 'vCode': VCODE}
  p = {}
  p.update(kwparams)
  print "ENDPOINT> ", endpoint
  pprint(p)
  xml = requests.get(endpoint, params=p)
  soup = BeautifulSoup.BeautifulSoup(xml.text)
  #print xml.text
  e = soup.findAll('error')
  if e:
    er = e[0]
    raise Exception(er.string)
    #raise EVEAPIException(er.string)
    #raise EVEAPIException(er.text, er.get('errorcode'), kwparams['keyID'], kwparams['vCode'])
    #ae.errortext = er.string
    #ae.errorcode = er.get('errorcode')
    #ae.keyid = kwparams['keyID']
    #ae.vcode = kwparams['vCode']
    #raise ae
  return soup

def getCharacters():
  xml = requests.get("https://api.eveonline.com/account/Characters.xml.aspx", params={'keyID':KEYID, 'vCode': VCODE})
  pprint(xml.text)
  soup = BeautifulSoup.BeautifulSoup(xml.text)
  return soup.findAll('row')

def getPlanets(characterid):
  xml = requests.get("https://api.eveonline.com/char/PlanetaryColonies.xml.aspx", params={'keyID':KEYID, 'vCode': VCODE, 'characterID': characterid})
  soup = BeautifulSoup.BeautifulSoup(xml.text)
  return soup.findAll('row')

def getPins(characterid, planetid):
  xml = requests.get("https://api.eveonline.com/char/PlanetaryPins.xml.aspx", params={'keyID':KEYID, 'vCode': VCODE, 'characterID': characterid, 'planetID': planetid})
  print xml.text
  soup = BeautifulSoup.BeautifulSoup(xml.text)

  return soup.findAll('row')

def getMembers():
  xml = requests.get("https://api.eveonline.com/corp/MemberTracking.xml.aspx", params={'keyID':KEYID, 'vCode': VCODE, 'characterID': characterid})
  soup = BeautifulSoup.BeautifulSoup(xml.text)
  return soup.findAll('row')


