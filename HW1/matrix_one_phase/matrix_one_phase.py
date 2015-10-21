mport MapReduce
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
    i_in_a=5
    j_in_bc=5
    k_in_c=5
    for k in range(0,k_in_c):
      mr.emit_intermediate((record[0],k),['A',record[1],record[2]])

    for i in range(0,j_in_bc):
      mr.emit_intermediate((i,record[1]),['B',record[0],record[2]])

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    length=len(list_of_values)
    total=0
    for x in range(0,length-1):
      for y in range(x+1,length):
        if list_of_values[x][0]!=list_of_values[y][0]:
          if list_of_values[x][1]==list_of_values[y][1]:
            prod=list_of_values[x][2]*list_of_values[y][2]
            total+=prod
    mr.emit([key[0],key[1],total])
  
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

