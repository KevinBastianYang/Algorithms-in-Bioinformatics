#! /usr/bin/python
"""
515111910078 yangjunchen
File_name: demo.py
Usage: python demo.py
demo.py is used for user to input a k to get a read map(e.g. seq_id_k9.map in demo_result folder) 
and summarized statistics of corresponding k(e.g. count_k9.txt ,also in demo_result folder)
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

			tmp = sorted(score,reverse=True)
			#note :  if the maximum score - the second / second score < 0.05, this read will not be assigned
			if abs(float(tmp[0] - tmp[1]) / tmp[1]) > 0.05:

				matchindex.append(score.index(tmp[0]))
			else:
				matchindex.append(10)
			read = file2.readline()
	file2.close()
	return matchindex

def main():
	k = input("please input k:(suggest 9 , 10, 11)\n")
	geno_set = []
	mat_set = []

	#construct matrixes
	for i in range(0,10):
		filename = "./genomes/"+str(i)+".fna"
		nametmp,mattmp = kmm_matrix(k,filename)
		geno_set.append(nametmp)
		mat_set.append(mattmp)
	geno_set.append("not assigned")
	#assign the read
	matchindex = read_match(k,"reads.fa",mat_set)
	#output the readmap
	file = open("./demo_result/seq_id_k"+str(k)+".map",'w')
	file_count = open("./demo_result/count_k"+str(k)+".txt",'w')
	for i, match in enumerate(matchindex):
		file.write(str(i))
		file.write('\t')
		file.write(geno_set[match])
		file.write('\n')
	file.close()
	#output the summarized statistics
	file_count.write("reads number\tgroup\n")
	for i in range(0,11):
		file_count.write(str(matchindex.count(i)))
		file_count.write('\t')
		file_count.write(geno_set[i])
		file_count.write('\n')
	file_count.close()
	
main()
