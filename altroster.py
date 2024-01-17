from tapiapi import * 
o = open('altreport.csv', 'w')

r = TESTgetGroupMembers(357) 
for u in r['users']:
  rr = getUser(u)
  for c in rr['characters']:
    o = c['name'].strip() + "," +  u.strip() + '\n'
    print o
    o.write(o + '\n')

o.flush()
o.close()

