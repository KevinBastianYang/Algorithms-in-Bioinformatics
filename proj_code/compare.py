#! /usr/bin/python
"""
515111910078 yangjunchen
File_name: compare.py
Usage: python compare.py
compare.py is used to see the assignment accurary among different k
"""
filenames = []
for i in range(3,12):
	filenames.append("./test_result/seq_id_k"+str(i)+".map")
for i,filename in enumerate(filenames):
	file = open(filename,'r')

	with open("./test_result/seq_id.map",'r') as file2:
		line2 = file2.readline()
		corre = 0
		count = 0
		while line2:
			line1 = file.readline()
			if line1 == line2:
				corre += 1
				count += 1
			else:
				count+=1
			line2 = file2.readline()
	print "--------"
	print "k = ", i+3
	print "Accurary: ",float(corre)/count