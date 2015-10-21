import MapReduce
import sys
import re
from collections import Counter

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    #words=re.search(r'\w+', values)
    words = re.findall(r'\w+',value)
    for w in words:
      mr.emit_intermediate(w.lower(),key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0
    c=Counter()
    for v in list_of_values:
      c[v] += 1 
    final_list=[] 
    for x in c:
      inner_list=[]
      inner_list.append(x)
      inner_list.append(c[x])
      final_list.append(inner_list)   
    mr.emit([key,len(c),final_list])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

