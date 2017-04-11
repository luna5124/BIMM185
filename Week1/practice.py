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
				left = line[1]
				my_max = float(line[-1])
		else:
			if my_max != 0:
	#			print(right, left, my_max)
				if count in counts:
					counts[count].append((right, left,my_max))
				else:
					counts[count]=[(right, left, my_max)]
			if protein == 2000:
				break
			right = line[0]
			my_max = float(line[-1])
			left = line[1]
			count = 1
			protein += 1
	#if count in counts:
	#	counts[count].append((right, left,my_max))
        #else:
        #        counts[count]=[(right, left, my_max)]

	for key in sorted(counts.keys(), reverse=True):
		for i in range(len(counts[key])):
			my_tuple = counts[key][i]
			#print my_tuple[0],'\t',my_tuple[1],'\t',float(my_tuple[2]),'\t', key
			print my_tuple, '\t', key


