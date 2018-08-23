#!/usr/bin/python
import sys
import re

def readin():
	parameters = sys.argv
	error = 0
	if len(parameters) == 1:
		error = 1
		return "Usage:python protsite.py pattern filename   ----note:please use a \" \" to quote your pattern ",error
	elif len(parameters) != 3:
		error = 2
		return "Error: Too many or too less parameters",error
	else :
		return parameters,error

def transit(p_pattern):
	amino_acid = "ACDEFGHIKLMNPQRSTVWY"

	p_pattern = p_pattern.replace('\\','').strip().split('-')

	r_pattern = ""

	prefix = "^\>[\w\.]+\s+\w+\s+(?P<name>\w+)\s+(?P<description>(\S{1,40}\s+){2,7})(?P<preaa>[ACDEFGHIKLMNPQRSTVWY]*)"
	flag = 0
	error = 0

	if p_pattern[-1][-1] != '.':
		error = 1
		return prefix,"Ending label '.'",error
	p_pattern[-1]= p_pattern[-1].rstrip('.')


	for pat in p_pattern:
		if pat[0] == '<':
			r_pattern+="^"
			pat = pat[1:]
		if pat[-1] == '>':
			flag = 1
			pat.replace('>','')

		if pat[0] == 'x':
			if len(pat) == 1:
				r_pattern+="[ACDEFGHIKLMNPQRSTVWY]"
			elif pat[1] == '(' and pat[-1] == ')':
				number = pat[2:-1].split(',')
				if len(number) == 1 and number[0].isdigit():
					r_pattern+="[ACDEFGHIKLMNPQRSTVWY]{"+number[0]+"}"
				elif len(number) == 2 and number[0].isdigit() and number[1].isdigit():
					r_pattern+="[ACDEFGHIKLMNPQRSTVWY]{"+number[0]+","+number[1]+"}"
				else:
					error = 1
					return prefix,pat,error
			else:
				error = 1	
				return prefix,pat,error
		elif pat[0] in amino_acid:
			if len(pat) == 1:
					r_pattern += pat[0]
			elif len(pat) ==2 and pat[1] == '>':
					r_pattern+=pat[0]+'\\n'
			elif pat[1] == '(' and pat[-1] == ')':
				if pat[2:-1].isdigit():
					r_pattern+=pat[0]+'{'+pat[2:-1]+'}'
				else:
					error = 1
					return prefix,pat,error	
			else:
					error = 1	
					return prefix,pat,error

		elif pat[0] == '[':
			if pat[-1] != ']':
				error = 1
				return prefix,pat,error
			for letter in pat[1:-2]:
				if letter not in amino_acid:
					error = 1	
					return prefix,pat,error	
			if pat[-2] in amino_acid:
				r_pattern+=pat
			elif pat[-2] == '>':
				r_pattern+='('+pat[1:-2]+'|'+"\\n"+')'

		elif pat[0] == '{':
			for letter in pat[1:-1]:
				if letter not in amino_acid:
					error = 1
					return prefix,pat,error	
			if pat[-1] != '}':
				error = 1
				return prefix,pat,error		
			else :
				r_pattern+="[^"+pat[1:-1]+']'
		
	return prefix, r_pattern,error

"""scanner(pre,flag,filename): scan the file for the regular expression"""
def scanner(pre,flag,filename):
	"""pattern is the merged final regex"""
	pattern = pre + '(?P<match>' + flag + ')'
	"""allline is the file content that remove unnessary \n in a sequence"""
	allline = ""

	file = open(filename,'r')
	for line in file.readlines():
		if line[0] != '>':
			allline+=line.strip('\n')
		else :
			allline+=line
	allline = allline.replace('>','\n>')
	
	"""search the regular expression"""
	pat = re.compile(pattern,re.M)
	result =  pat.finditer(allline)
	"""print the result"""
	for item in result:
		pos_start = len(item.group('preaa').replace('\n',''))
		print "Start    End    Name    Description"
		print pos_start,"    ",pos_start + len(item.group('match').replace('\n',''))-1, "    ",item.group('name').replace('\n',''),"    " ,item.group('description').replace('\n','')

def main():
	para,err = readin()
	if err == 1: 
		print para
	elif err == 2:
		print para		
	else:
		prefix , subfix, error = transit(para[1])
		if (error == 1) :
			print subfix, "maybe wrong or missing, please check! "
		else:
			scanner(prefix,subfix,para[2])
main()

