#Please note:
#Right is the protein in the first column(left)
#Left is the second column(right) in the input file.
#Since the usage of these two variables are consistent throughout the code, 
#I decided to keep it as it was
with open('RS.txt','r') as file:
	right = ""
	left = ""
	my_max = 0
	count = 1
	protein = 0
	counts = {}
	for line in file:
		line = line[:-1].split('\t')
		if right == line[0]:
			count += 1
			if float(line[-1]) > my_max:
				#if the possiblily of the readin pair is higher than the pairs with the same reference protein
				left = line[1]
				my_max = float(line[-1])
		else:
			if my_max != 0:
				#print(right, left, my_max)
				if count in counts:
					counts[count].append((right, left,my_max))
				else:
					counts[count]=[(right, left, my_max)]
			if protein == 2000:
				break
			#initilization when hit a new reference protein 
			right = line[0]
			my_max = float(line[-1])
			left = line[1]
			count = 1
			protein += 1
	#if count in counts:
	#	counts[count].append((right, left,my_max))
        #else:
        #        counts[count]=[(right, left, my_max)]

    #in decending order of the number of interecting pairs
	for key in sorted(counts.keys(), reverse=True):
		for i in range(len(counts[key])):
			my_tuple = counts[key][i]
			#print my_tuple[0],'\t',my_tuple[1],'\t',float(my_tuple[2]),'\t', key
			print my_tuple, '\t', key


