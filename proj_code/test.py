#! /usr/bin/python
"""
515111910078 yangjunchen
File_name: test.py
Usage: python test.py
Use the given 20000 reads to test the model by using different k(3-11).
The assigned map for different k will be in test_result folder.
Another file compare.py can be used to see the assignment accurary.
"""
import numpy as np 
from itertools import product
from collections import Counter
from math import log


#read the genome file,construct a 4**k * 4 transition probability matrix
def kmm_matrix(k,filename1):
	file1 = open(filename1,'r')
	genome_name = file1.readline().strip('\n').split('|')[4].strip()
	line = file1.readline()
	#get genome
	genoseq = ''
	while line:
		genoseq += line.strip('\n').replace("B","C").replace("D","A").replace("H","A").replace("K","G").replace("M","A").replace("N","A").replace("R","A").replace("S","C").replace("V","A").replace("W","A").replace("Y","C")
		line = file1.readline()
	#initialize
	matrix = np.ones((4**k,4),dtype = float)

	#index ATGC combinations by using a dictionary
	dic ={}
	for i,item in enumerate(product('ATGC',repeat=k)):
		sumstr = ''
		for j in range(0,len(item)):
			sumstr+=item[j]
		dic[sumstr] = i
	first_dic = {'A':0,'T':1,'G':2,'C':3}

	#calculate the transition frequency
	for i in range(0,len(genoseq)-k):
		matrix[dic[genoseq[i:i+k]]][first_dic[genoseq[i+k]]] += 1.0
	#calculate the probability
	for i in range(0,4**k):
		rowsum = sum(matrix[i][j] for j in range(0,4))
		for m in range(0,4):
			matrix[i][m]= log(matrix[i][m]/ rowsum,2)
	file1.close()
	return genome_name, matrix

#for each read, select the max matching score among 10 matrixes,return the corresponding index
def read_match(k,filename2,mat_set):
	file2 = open(filename2,'r')
	read = file2.readline()
	matchindex = []
	first_dic = {'A':0,'T':1,'G':2,'C':3}
	#index
	dic ={}
	for i,item in enumerate(product('ATGC',repeat=k)):
		sumstr = ''
		for j in range(0,len(item)):
			sumstr+=item[j]
		dic[sumstr] = i
	count = 0

	while read:
		if read[0] == '>':
			read = file2.readline()
			continue
		else:
			count += 1
			read = read.strip('\n').replace("B","C").replace("D","A").replace("H","A").replace("K","G").replace("M","A").replace("N","A").replace("R","A").replace("S","C").replace("V","A").replace("W","A").replace("Y","C")
			score = []
			for mat in mat_set:
				score.append(float(sum(mat[dic[read[i:i+k]]][first_dic[read[i+k]]] for i in range(0,len(read)-k))))			
			matchindex.append(score.index(max(score)))
			read = file2.readline()
	file2.close()
	return matchindex

def main():
	print "Test: use different k(ranging from 3 to 11) to tackle the test reads, it takes a while..."
	print "the assigned situation is in test_result folder, seq_id_k3,map, seq_id_k4.map ..etc"
	print "you can use compare.py to compare each result to the original seq_id.map to see the accurary."
	#iterate different k
	for k in range(3,12):
		geno_set = []
		mat_set = []
		for i in range(0,10):
			filename = "./genomes/"+str(i)+".fna"
			nametmp,mattmp = kmm_matrix(k,filename)
			geno_set.append(nametmp)
			mat_set.append(mattmp)
		matchindex = read_match(k,"test.fa",mat_set)

		file = open("./test_result/seq_id_k"+str(k)+".map",'w')
		#use the index to find the genome name
		for i, match in enumerate(matchindex):
			file.write(str(i))
			file.write('\t')
			file.write(geno_set[match])
			file.write('\n')
		file.close()
main()
