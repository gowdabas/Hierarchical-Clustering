mport sys

input=sys.argv[1]
output=sys.argv[2]
inputfile=open(input)
outputfile=open(output,'w')
for each in inputfile:
	words=each.split()
	count=0
	for i in words:
		count=count+1
	print count
	outputfile.write(str(count)+'\n')	
	
inputfile.close()
outputfile.close()



