import sys, traceback
#from api import *
from pprint import pprint
import BeautifulSoup, requests
requests.packages.urllib3.disable_warnings()

class APIException(Exception):
  pass

def getAPIKeyInfo(kwparams):
  endpoint = 'https://api.eveonline.com/account/APIKeyInfo.xml.aspx'
  #p = {'keyID':KEYID, 'vCode': VCODE}
  p = {}
  p.update(kwparams)
  xml = requests.get(endpoint, params=p)
  soup = BeautifulSoup.BeautifulSoup(xml.text)
  print xml.text
  e = soup.findAll('error')
  if e:
    er = e[0]
    ae = APIException(er.text)
    ae.errortext = er.text
    ae.errorcode = er.get('errorcode')
    ae.keyid = kwparams['keyID']
    ae.vcode = kwparams['vCode']
    raise ae
  return soup

f = open(sys.argv[1], 'r').read()
output = open('keyreport.csv', 'w')
for l in f.split('\n'):
  try:
    print l
    keyid,vcode = l.split(' ')
    chars = []
    r = getAPIKeyInfo({'keyID': keyid, 'vCode': vcode})
    k = r.findAll('key')
    mask = k[0].get('accessmask', '')
    expires = k[0].get('expires', '')
    keytype = k[0].get('type', '')
    rows = r.findAll('row')
    chars = [(rr.get('charactername'), rr.get('corporationname'), rr.get('characterid')) for rr in rows]
    for char in chars:
      outv = "%s,%s,%s,%s,%s,%s,%s,%s\n" % (keyid, vcode, char[2], char[0], char[1], mask, expires, keytype)
      output.write(outv)
  except Exception as e:
    traceback.print_exc()
  except APIException as e:
    outv = "%s,%s,,,,%s,%s\n" % (e.keyid, e.vcode, e.errorcode, e.errortext) 
    output.write(outv)
