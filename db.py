import sqlite3, pprint, sys

s = sqlite3.connect('eve.db')

#(u'table', u'invmarketgroups', u'invmarketgroups', 9, u'CREATE TABLE invmarketgroups (\n\t"marketGroupID" INTEGER NOT NULL, \n\t"marketGroupName" VARCHAR, \n\tdescription VARCHAR, \n\t"hasTypes" BOOLEAN, \n\t"parentGroupID" INTEGER, \n\t"iconID" INTEGER, \n\tPRIMARY KEY ("marketGroupID"), \n\tCHECK ("hasTypes" IN (0, 1)), \n\tFOREIGN KEY("parentGroupID") REFERENCES invmarketgroups ("marketGroupID") DEFERRABLE INITIALLY DEFERRED, \n\tFOREIGN KEY("iconID") REFERENCES icons ("iconID")\n)#)

def marketSubGroupsByName(marketgroupname):
  """ Return all the subgroups of a group specified by name """
  r = s.execute("select marketGroupID from invmarketgroups where marketGroupName = ?", (marketgroupname,))
  gid = None
  for l in r:
    gid = l[0]
  if not gid:
    raise Exception("Market group not found:", marketgroupname)
  
  sub = marketSubGroups(gid)
  return sub

def marketSubGroups(marketgroupid):
  """ Given a marketgroupid return all marketgroupids below it, and including it. """
  r = s.execute("select marketGroupID, marketGroupName from invmarketgroups where parentGroupID = ?", (marketgroupid,))
  retval = set()
  retval.add(marketgroupid)
  for l in r:  
    sgid = l[0]
    retval.add(sgid)
    sub = marketSubGroups(sgid)
    if len(sub) > 0:
      retval.update(sub)
  return retval

def itemsByGroups(groups):
  r = s.execute("select marketGroupID, typeName, typeID from invTypes")
  retval = set()
  for l in r:
    if l[0] in groups:
      retval.add(l[1])
  return retval

def itemGroup(itemname):
  r = s.execute("select marketGroupID from invTypes where typeName = ?", (itemname, ))
  for l in r:
    rr = s.execute("select marketGroupName from invmarketgroups where marketGroupID = ?", (l[0], ))
    for ll in rr:
      print ll[0]

if __name__ == '__main__':
  itemGroup(sys.argv[1])

