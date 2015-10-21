import MapReduce
import sys
import re
import itertools
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
    #key = record[0]
    value = record
   # words=value.split(',')
    #for w in words:
    pair=itertools.combinations(value,2)
    for x in pair:
      mr.emit_intermediate(x,1)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
      total+=v 
    if total>=100:       
      mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

