import sys
import numpy
import heapq
import math
import itertools



def find_centroid(cluster,points_list):
	centroid=[]
	cluster_length=len(cluster)
	cluster_list_for_centroid=[]

	for i in range(0,dimension):
		centroid.append(0.0)

	for i in range(0,cluster_length):
		cluster_list_for_centroid.append(points_list[cluster[i]])


	for i in range(0,dimension):
		for j in range(0,cluster_length):
			centroid[i]+=cluster_list_for_centroid[j][i]
		centroid[i]=centroid[i]/cluster_length	
	return centroid	


def Euclidean_distance(clusterA,clusterB,points_list):
	sum_squared=0

	#print clusterA
	if len(clusterA)==1:
		centroidA=points_list[clusterA[0]]
	else:
		centroidA=find_centroid(clusterA,points_list)

	if len(clusterB)==1:
		centroidB=points_list[clusterB[0]]
	else:
		centroidB=find_centroid(clusterB,points_list)		
	
	for i in range(0,dimension):
		x=centroidA[i]
		y=centroidB[i]

		sum_squared+=pow((x-y),2)
	euclidean_dist=math.sqrt(sum_squared)
	
	return euclidean_dist	


def find_new_cluster_pairwise_distance(i,index_list,points_list,heap):
	clusterA=list(index_list[i])
	j=i+1
	for k in range(j,len(index_list)):
		clusterB=list(index_list[k])
		dist=Euclidean_distance(clusterA,clusterB,points_list)
		dist_list=[dist,[clusterA,clusterB]]
		heapq.heappush(heap,dist_list)
	return heap	


def merge_clusters(clusterA,clusterB):
	return sorted(list(set(clusterA) | set(clusterB)))				

def clustering(heap,n):
	
	clusters_dict={}
	
	while n>1:
		
		closest_cluster=heapq.heappop(heap)
		cluster1=closest_cluster[1][0]
		cluster2=closest_cluster[1][1]

		if cluster1 in index_list and cluster2 in index_list:
			index_list.remove(cluster1)
			index_list.remove(cluster2)
			merged_cluster=merge_clusters(cluster1,cluster2)
			index_list.insert(0,merged_cluster)
			heap=find_new_cluster_pairwise_distance(0,index_list,points_list,heap)
			n=n-1
			clusters_dict[n]=list(index_list)

	return clusters_dict		



def setup_input(n):
	cluster_list=[]
	dist_list=[]
	heap=[]
	#print points_list
	for i in range(0,n-1):
		heap=find_new_cluster_pairwise_distance(i,index_list,points_list,heap)
	return heap		

def gold_std(lines):
	gold_std_dict={}

	index=0
	for each in lines:
		point=each.strip().split(',')
		cluster_name=point[-1]

		gold_std_dict.setdefault(cluster_name,[])
		gold_points_list=gold_std_dict[cluster_name]
		gold_points_list.append(index)
		gold_std_dict[cluster_name]=gold_points_list
		index+=1

	return gold_std_dict

def precision_and_recall(my_pairs,gold_pairs):
	common_pairs=set(my_pairs).intersection(gold_pairs)

	my_pairs_count=float(len(my_pairs))
	gold_pairs_count=float(len(gold_pairs))
	common_pairs_count=float(len(common_pairs))

	precision=common_pairs_count/my_pairs_count
	recall=common_pairs_count/gold_pairs_count

	return precision, recall



def create_pairs(pairs,cluster):
	new_pairs=list(itertools.combinations(cluster,2))
	pairs=pairs+new_pairs
	return pairs

def accuracy(k_clusters,lines):
	my_pairs=[]
	gold_pairs=[]
	for cluster in k_clusters:
		my_pairs=create_pairs(my_pairs,cluster)

	gold_std_dict=gold_std(lines)
		
	for key,value in gold_std_dict.items():
		gold_pairs=create_pairs(gold_pairs,value)

	precision,recall=precision_and_recall(my_pairs,gold_pairs)
	return precision,recall

def print_result(k_clusters,precision,recall):
	print precision
	print recall
	for i in range(0,len(k_clusters)):
		print k_clusters[i]


def main(lines,k):	
	global dimension
	dimension=0
	global points_list
	points_list=[]
	global index_list
	index_list=[]
	n=0
	for x in lines:
		data_point=x.strip().split(',')
		del data_point[-1]
		data_point=[float(i) for i in data_point]
		points_list.append(data_point)
		index_list.append([n])
		n+=1

	dimension=len(points_list[0])
	heap=setup_input(n)	
	clusters_dict=clustering(heap,n) 
	precision,recall=accuracy(clusters_dict[k],lines)
	print_result(clusters_dict[k],precision,recall)

				


input_data=open(sys.argv[1],'r')
lines=input_data.readlines()
k=int(sys.argv[2])
main(lines,k)