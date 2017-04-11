import re
with open('TCDB.faa','r') as file:
	start = False
	for line in file:
		line = line[:-1]
		m = re.search('>.*\|.*\|(\S+)\|(\S+)',line)
		if m:
			if start:
				print()
			else:
				start = True

			#line = line.split('|')
			#print(line[3].split()[0] + '-' + line[2] + '\t',end='')
			
			#use regular expression
			print(m.group(2) + '-' + m.group(1) + '\t',end='')
		else:
			print(line,end='')
