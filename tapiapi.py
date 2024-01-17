from credentials import *

import BeautifulSoup, requests, json
from pprint import pprint
requests.packages.urllib3.disable_warnings()

def getMemberAPIKey(charid):
  xml = requests.get("https://auth.pleaseignore.com/api/1.0/character", params={'apikey': TESTALLIANCEKEY, 'charid': charid})
  soup = BeautifulSoup.BeautifulSoup(xml.text)
  return soup

def testRequest(endpoint, params):
  params['apikey'] = TESTALLIANCEKEY 
  pprint(params)
  xml = requests.get("https://auth.pleaseignore.com/api/1.0/%s" % endpoint, params=params)
  #soup = BeautifulSoup.BeautifulSoup(xml.text)
  return json.loads(xml.text)

def getInfo():
  r = testRequest('info', {'request': 'groups'})

def TESTgetGroupMembers(groupid):
  r = testRequest('group', {'groupid': groupid})
  return r

def getUser(username):
  r = testRequest('user', {'user': username})
  return r

