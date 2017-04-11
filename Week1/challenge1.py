import re
with open('TCDB.faa','r') as file:
	start = False
	# read file line by line
	for line in file:

		line = line[:-1]#get rid of '\n' at the end of each line
    #the current line is a header
		m = re.search('>.*\|.*\|(\S+)\|(\S+)',line)
		if m:
			if start:
				#start a new line
				print()
			else:
				start = True


			#line = line.split('|')
			#print(line[3].split()[0] + '-' + line[2] + '\t',end='')
			
			#print use regular expression
			print(m.group(2) + '-' + m.group(1) + '\t',end='')
		
    #the current line is not a header
		else:
			print(line,end='')
