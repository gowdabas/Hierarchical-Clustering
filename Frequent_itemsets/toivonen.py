import sys
import re
import itertools
import random 
from collections import Counter



def make_subsets(item_set,k):
	pair=itertools.combinations(item_set,k)
	pair_list=list(pair)
	return pair_list

def create_samples(record,k,iterations):

	iterations=iterations+1
	#print iterations
	record.seek(0,0)
	
	sample = []
	linecount = sum(1 for line in record)
	record.seek(0)

	random_linenos = sorted(random.sample(xrange(linecount), k), reverse = True)
	lineno = random_linenos.pop()
	for n, line in enumerate(record):
		if n == lineno:
			sample.append(sorted(line.rstrip().split(',')))
			if len(random_linenos) > 0:
				lineno = random_linenos.pop()
			else:
				break
	return sample

def create_NBL(sample_list,k,Item_list,candidate_Item_List,NBL,candidate_freq_list):
	k_subsets=[]
	k_1_subsets=[]

	for item in sample_list:
		if len(item)>=k:
			k_subsets.append(make_subsets(item,k))
	
			for itemA in k_subsets:
				
				for itemB in itemA:
					if len(itemB)>1:
						
						if itemB in Item_list and itemB not in candidate_freq_list:	
								
							k_1_subsets=make_subsets(itemB,k-1) 
							#print Freq_Item_List 	
							flag=1
							for itemC in k_1_subsets:
								if len(itemC)==1:
									if itemC[0] not in candidate_Item_List:
										#print'b'
										flag=0
								else:
									if itemC not in candidate_Item_List:
										flag=0		
							if flag==1:
								#print 'a'
								if itemB not in NBL:
									NBL.append(itemB)

	return NBL	

def Apriori(sample_list,sample_support,k,candidate_Item_list):
	c_single=Counter()
	c_multi=Counter()
	Item_List=[]
	lists=[]
	intermediate_list=[]
	NBL=[]
	candidate_freq_list=[]
	
	if k==1:
		for item in sample_list:
			for each in item:
				c_single[each]+=1

		for x in c_single:
			if c_single[x]>=sample_support:
				if x not in Item_List:
					Item_List.append(x)	
			else:
				if x not in NBL:
					NBL.append(x)				

		lists=[]
		lists.append(Item_List)
		lists.append(NBL)		
		return lists

	else:
		for item in sample_list:
			if len(item)>=k:
				k_sets=sorted(make_subsets(item,k))

				for each in k_sets:
					c_multi[each]+=1
					k_1_subsets=sorted(make_subsets(each,k-1))
					#print each , k_1_subsets
					flag=0
					for item in k_1_subsets:
						#print item
						if len(item)==1:
							if item[0] not in candidate_Item_list:
								flag=1
						else:		
							if item not in candidate_Item_list:
								flag=1	
							
					if flag==0: 
						if each not in Item_List:
							Item_List.append(each)
		Item_List=sorted(Item_List)					
		for i in c_multi:
			if c_multi[i]>=sample_support:
				if  i in Item_List:
					#print 'b'
					candidate_freq_list.append(i)

		NBL=create_NBL(sample_list,k,Item_List,candidate_Item_list,NBL,candidate_freq_list)	
		lists=[]
		lists.append(candidate_freq_list)
		lists.append(NBL)	
		return lists						


def first_pass(record,support,linecount):
	
	c1=Counter()
	Freq_Item_List=[]
	freq_pairs=[]
	pair_list=[]
	entire_sample=[]
	negative_border_list=[]
	candidate_Item_list=[]
	
	support=int(support)
	num_of_lines_sample=linecount/2
	fraction=0.5
	sample_support=0.8*support*fraction
	
	final_list=[]
	k=1
	repeat=0
	x=0
	iterations=1
	sample_list=create_samples(record,num_of_lines_sample,iterations)
	
	while len(Freq_Item_List)>0 or k==1:
		if repeat==1:
			#print 'xyx'
			sample_list=create_samples(record,num_of_lines_sample,iterations)
			k=1	
			repeat=0
			candidate_Item_list=[]
			NBL=[]
			received_list=sorted(Apriori(sample_list,sample_support,k,sorted(candidate_Item_list)))
			#print 'candidate list', sorted(candidate_list)
			candidate_Item_list=sorted(received_list[0])
			NBL=received_list[1]


		else:
			
			received_list=sorted(Apriori(sample_list,sample_support,k,sorted(candidate_Item_list)))
			candidate_Item_list=received_list[0]
			NBL=received_list[1]

		#pass 2 
		del Freq_Item_List[:]
		c_item=Counter()								
		record.seek(0,0)
		for line in record:
			bucket=sorted(line.strip().split(','))
			pair_list=make_subsets(bucket,k)
			#print pair_list
			for item in pair_list:	
				itemZ=list(item)
				if len(itemZ)==1:
					if itemZ[0] in candidate_Item_list or itemZ[0] in NBL:
						c_item[item]+=1
				else:		
					if item in candidate_Item_list or item in NBL:
						c_item[item]+=1
		#print c_item
		for x in c_item:
			if c_item[x]>=support:
				if x not in Freq_Item_List:
					if len(x)==1:
						Freq_Item_List.append(x[0])
					else:
						Freq_Item_List.append(x)
		change=0
	
		for each in NBL:
			if each in Freq_Item_List:
				change=1		
		
		if len(Freq_Item_List)>0:
			temp_list=[]
			for each in Freq_Item_List:
				item=list(each)
				temp_list.append(item)
			final_list.append(sorted(temp_list))

		if change==1:
			repeat=1
			iterations=iterations+1
			del final_list[:]

		else:
			k=k+1
	print iterations
	print fraction
	for i in range(0,len(final_list)):
		print final_list[i]







inputdata=open(sys.argv[1],'r')
linecount=sum(1 for line in inputdata)
support=sys.argv[2]
first_pass(inputdata,support,linecount)
