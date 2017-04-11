with open('first2.txt','r') as file:
	start = False
	for line in file:
		line = line[:-1]
		if ">" in line:
			if start:
				print()
			else:
				start = True
			line = line.split('|')
			print(line[3].split()[0] + '-' + line[2] + '\t',end='')
		else:
			print(line,end='')
