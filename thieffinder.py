import csv, traceback, sys
from api import eveApi

def walkApi(endpoint, params, refparam):
  try:
    r = eveApi(endpoint, params)
  except:
    traceback.print_exc()
  rows = r.findAll('row')
  while rows:
    for row in rows:
      yield row
  
    refid = rows[-1].get(refparam)
    if not refid:
      return
    np = dict(params)
    np['fromID'] = refid
    r = eveApi(endpoint, np)
    rows = r.findAll('row')
 
def runReport(keyid, vcode, charid):
  try:
    o = open('evidence/%s_items.xml' % charid, 'w')
    r = eveApi('/char/AssetList.xml.aspx', {'keyID': keyid, 'vCode': vcode, 'characterID': charid})
    o.write(str(r))
    o.flush(); o.close()
  except:
    traceback.print_exc()

  try:
    o = open('evidence/%s_contracts.xml' % charid, 'w')
    r = eveApi('/char/Contracts.xml.aspx', {'keyID': keyid, 'vCode': vcode, 'characterID': charid})
    o.write(str(r))
    o.flush(); o.close()
  except:
    traceback.print_exc()

  for rr in r.findAll('row'):
    try:
      cid = rr.get('contractid')
      o = open('evidence/%s_contracts_%s.xml' % (charid, cid), 'w')
      r = eveApi('/char/ContractItems.xml.aspx', {'keyID': keyid, 'vCode': vcode, 'contractID': cid, 'characterID': charid})
      o.write(str(r))
      o.flush(); o.close()
    except:
      traceback.print_exc()
 
  try:
    o = open('evidence/%s_items.xml' % charid, 'w')
    r = eveApi('/char/AssetList.xml.aspx', {'keyID': keyid, 'vCode': vcode, 'characterID': charid})
    o.write(str(r))
    o.flush(); o.close()
  except:
    traceback.print_exc()
 
  o = open('evidence/%s_journal.xml' % charid, 'w')
  for row in walkApi('/char/WalletJournal.xml.aspx', {'keyID': keyid, 'vCode': vcode, 'characterID': charid}, 'refid'):
    o.write(str(r) + '\n')
  o.flush(); o.close()

  o = open('evidence/%s_wallettxact.xml' % charid, 'w')
  for row in walkApi('/char/WalletTransactions.xml.aspx', {'keyID': keyid, 'vCode': vcode, 'characterID': charid}, 'transactionid'):
    o.write(str(r) + '\n')
  o.flush(); o.close()
   
reader = csv.reader(open('keyreport.csv'))
for r in reader:
  try:
    runReport(r[0], r[1], r[2])
  except KeyboardInterrupt:
    sys.exit(-1)
  except:
    traceback.print_exc()
