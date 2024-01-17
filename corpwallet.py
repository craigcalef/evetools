from api import *

r = eveCorpApiRequest('/corp/WalletJournal.xml.aspx')
rows = r.findAll('row')
while rows:
  #date="2015-08-02 17:06:40" refid="11489441915" reftypeid="96" ownername1="Bottom Truck" ownerid1="95259528" ownername2="Sleeper Slumber Party" ownerid2="98312583" argname1="J113701 II" argid1="40455488" amount="233940.00" balance="11947075835.76" reason="Import Duty for J113701 II" owner1typeid="1373" owner2typeid="2">
  for row in rows:
    print ",".join([ row.get('date'), row.get('ownername1'), row.get('amount'), row.get('balance')]) 

  refid = rows[-1].get('refid')
  r = eveCorpApiRequest('/corp/WalletJournal.xml.aspx', {'fromID': refid})
  rows = r.findAll('row')
