with open('first2.txt','r') as file:
	start = False
	# read file line by line
	for line in file:
		line = line[:-1]#get rid of '\n' at the end of each line
		#the current line is a header
		if ">" in line:
			if start:
				#start a new line
				print()
			else:
				start = True
			line = line.split('|')
			print(line[3].split()[0] + '-' + line[2] + '\t',end='')
		#the current line is not a header
		else:
			print(line,end='')
