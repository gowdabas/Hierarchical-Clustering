import sys
import re
import itertools
from collections import Counter


def hash_value_calculation(pair,hash_func,c,bucket_size):
	sum=0
	for i in pair:
		sum=sum+c[i]
	if hash_func[0]=='+' and hash_func[1]=='%':
		hash_value=sum%bucket_size
		return hash_value	


def make_subsets(item_set,k):
	pair=itertools.combinations(item_set,k)
	pair_list=list(pair)
	#`print pair_list
	return pair_list


def first_pass(record,support,bucket_size,hash_func):
	hash_map={}
	c=Counter()
	hash_dict={}
	bucket_count=0
	support=int(support)
	Freq_Item_List=[]
	
	for i in range(0,bucket_size):
		hash_dict.setdefault(i,0)
	
	for line in record:
		bucket=sorted(line.strip().split(','))
		
		#print pair_list
		for item in bucket:
			c[item]+=1
			#print c
			# list elements with count > suppport  i.e FIL
		for x in c:
			if c[x]>=support:
				if x not in Freq_Item_List:
					Freq_Item_List.append(x)

	print Freq_Item_List
	k=2
	while len(Freq_Item_List)>0:
		record.seek(0,0)
		for line in record:
			bucket=sorted(line.strip().split(','))
			pair_list=make_subsets(bucket,k)
			for each_pair in pair_list:
				hash_value=hash_value_calculation(each_pair,hash_func,c,bucket_size)
				if hash_value in hash_dict.keys():
					hash_dict[hash_value]+=1
				else:
					hash_dict[hash_value]=1	
		new_final_dict=dict(hash_dict)
		#print new_final_dict
	

		for key,value in hash_dict.items():
			if hash_dict[key]>=support:
				#print 'a'
				hash_dict[key]=1
			else:
				#print 'b'
				hash_dict[key]=0
		#print hash_dict

		candidate_list=[]
		record.seek(0,0)
		#print Freq_Item_List
		for line in record:
			bucket=sorted(line.strip().split(','))
			#print bucket
			pair_list=make_subsets(bucket,k)
			#print pair_list

			for each_pair in list(pair_list):
				#print each_pair
				flag=1
				subset_list=list(each_pair)
				#subset_list=pairs.split(',')
				#print subset_list
				klist=make_subsets(subset_list,k-1)
				#print klist
				for item in klist:
					new_item=list(item)
					if len(new_item)==1:
						if new_item[0] not in Freq_Item_List:
							flag=0
					else:
						if new_item not in Freq_Item_List:
							flag=0	
					if flag==1:
						hash_value=hash_value_calculation(each_pair,hash_func,c,bucket_size)
						if hash_value in hash_dict.keys() and hash_dict[hash_value]==1:
							if list(each_pair) not in candidate_list:
								candidate_list.append(list(each_pair))
				    


		del Freq_Item_List[:]
		c_item=Counter()
		record.seek(0,0)
		for line in record:
			bucket=sorted(line.strip().split(','))
			pair_list=make_subsets(bucket,k)
			for item in pair_list:
				if list(item) in candidate_list:
					c_item[item]+=1
		for x in c_item:
			if c_item[x]>=support:
				if x not in Freq_Item_List:
					Freq_Item_List.append(list(x))
		if len(Freq_Item_List)>0:
			print new_final_dict
			print sorted(Freq_Item_List)			
		k=k+1	




inputdata=open(sys.argv[1],'r')
support=sys.argv[2]
bucket_size=int(sys.argv[3])
hash_func=['+','%']
first_pass(inputdata,support,bucket_size,hash_func)

