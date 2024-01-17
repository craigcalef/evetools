
import sys

AuToKm = 149597870.6
maxscan = 2139249551
def normalize_distance(r):
  dist = 0
  if r[2] == '-':
    dist = 0
  else:
    dist_txt = r[2]
    dist_txt = dist_txt.replace(',', '')
    if dist_txt.endswith('AU'):
      dist = round(float(dist_txt.split(' ')[0]) * AuToKm)
    if dist_txt.endswith(' m'):
      dist = round(int(dist_txt.split(' ')[0]) / 1000)
  return (r[0], r[1], dist)
 
def input_dscan():
  allbuffer = []
  l = raw_input()
  while l != ".":
    allbuffer.append(l.strip())
    l = raw_input()

  results = set()
  dupes = set()
  
  for l in allbuffer:
    r = l.split('\t')
    if len(r) == 3:
      r = normalize_distance(r) 
      if not r in results:
        if not r in dupes:
            results.add(r) 
      else:
        results.remove(r)
        dupes.add(r)
  return results, dupes

print "Enter ALL dscan (end with '.')"
all_r, all_d = input_dscan()

target = (0,0)
while len(target) != 3:
  print "Enter target dscan line"
  target_line = raw_input().strip()
  target = target_line.split('\t')
  target = normalize_distance(target)

#set up "goal-posts"

post_a = 0
post_b = maxscan

while True:
  midpoint = post_a + round((post_b - post_a) / 2)
  #print "Scan this value (%f AU)" % midpoint / AuToKm
  print "Scan this value: %.0f" % midpoint

  print "Paste new dscan"
  update_results, update_dupes = input_dscan()

  #closest = min(update_results, key=lambda x: abs(int(x[2]) - midpoint))
  #print "Closest entry: %s - %s  
  closest_known = filter(lambda x: x[2] > 0, update_results)
  rang = [(e[0], e[1], abs(int(e[2]) - midpoint)) for e in closest_known]
  rang.sort(key=lambda x: x[2], reverse=True)
  for r in rang[:-5]:
    print r[0], '-', r[1], ' = ', r[2]
 
  print "->", type(post_b), type(post_a)
  print "Deviation:", post_b - post_a

  if target in update_results:
    post_b = int(midpoint)
  else:
    post_a = int(midpoint)

