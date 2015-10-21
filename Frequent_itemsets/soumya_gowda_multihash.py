import sys
import re
import itertools
from collections import Counter



def hash_value_calculation(pair,hash_func,c,bucket_size):
	item_sum=0
	product=1
	for i in pair:
		item_sum=item_sum+c[i]
	for j in pair:
		product=product*c[j]	
	if hash_func[0]=='+' and hash_func[1]=='%':
		hash_value=item_sum%bucket_size
		return hash_value
	if hash_func[0]=='*' and hash_func[1]=='%':
		hash_value=product%bucket_size	
		return hash_value
	
		

def make_subsets(item_set,k):
	pair=itertools.combinations(item_set,k)
	pair_list=list(pair)
	return pair_list


def first_pass(record,support,bucket_size,first_hash_func,sec_hash_func):
	hash_map={}
	c=Counter()
	first_dict={}
	sec_dict={}
	bucket_count=0
	Freq_Item_List=[]
	support=int(support)
	for i in range(0,bucket_size):
		first_dict.setdefault(i,0)
	for i in range(0,bucket_size):
		sec_dict.setdefault(i,0)
		

	for line in record:
		bucket=sorted(line.strip().split(','))

		for item in bucket:
			c[item]+=1
		for x in c:
			if c[x]>=support:
				if x not in Freq_Item_List:
					Freq_Item_List.append(x)

	print sorted(Freq_Item_List)

	k=2
	while len(Freq_Item_List)>0:
		record.seek(0,0)
		for line in record:
			bucket=sorted(line.strip().split(','))
			pair_list=make_subsets(bucket,k)
			#print bucket
			for each_pair in pair_list:
				#print each_pair
				hash_value=hash_value_calculation(each_pair,first_hash_func,c,bucket_size)
				#print hash_value
				if hash_value in first_dict.keys():
					first_dict[hash_value]+=1
				else:
					first_dict[hash_value]=1

			for each_pair in pair_list:
				#print each_pair
				hash_value=hash_value_calculation(each_pair,sec_hash_func,c,bucket_size)
				#print hash_value
				if hash_value in sec_dict.keys():
					sec_dict[hash_value]+=1
				else:
					sec_dict[hash_value]=1	
		#print first_dict
		#print sec_dict			
		new_first_dict=dict(first_dict)				
		new_sec_dict=dict(sec_dict)
		#print new_first_dict
		#print new_sec_dict

		for key,value in first_dict.items():
			if first_dict[key]>=support:
				first_dict[key]=1
			else:
				first_dict[key]=0

		for key,value in sec_dict.items():
			if sec_dict[key]>=support:
				sec_dict[key]=1
			else:
				sec_dict[key]=0	

		#print first_dict
		#print sec_dict		
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
					k_1_list=make_subsets(subset_list,k-1)
					#print 'klist'
					#print klist
					for item in k_1_list:
						new_item=list(item)
						if len(new_item)==1:
							#print new_item[0]
							if new_item[0] not in Freq_Item_List:
								flag=0
						else:
							if new_item not in Freq_Item_List:
								flag=0	
					if flag==1:
						#print each_pair
						first_hash_value=hash_value_calculation(each_pair,first_hash_func,c,bucket_size)
						#print first_hash_value
						sec_hash_value=hash_value_calculation(each_pair,sec_hash_func,c,bucket_size)
						#print sec_hash_value
						if first_dict[first_hash_value]==1 and sec_dict[sec_hash_value]==1: #check if its already there later
							if list(each_pair) not in candidate_list:
								candidate_list.append(list(each_pair))
		#print 'a'					
		#print candidate_list					
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
			print new_first_dict
			print new_first_dict
			print sorted(Freq_Item_List)			
		k=k+1						
	



inputdata=open(sys.argv[1],'r')
support=sys.argv[2]
bucket_size=int(sys.argv[3])
first_hash_func=['*','%']
sec_hash_func=['+','%']
first_pass(inputdata,support,bucket_size,first_hash_func,sec_hash_func)
