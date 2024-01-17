def pairs(l):
  """ Given a list, pair the items in the list and return it as a list of tuples """
  for i in xrange(0, len(l), 2):
    yield l[i:i+2]

