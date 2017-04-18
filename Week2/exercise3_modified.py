genome = ""
with open("GCF_000005845.2_ASM584v2_genomic.fna",'r') as file:
	file.readline()
	for line in file:
		line = line[:-1]
		genome = genome + line

#print(len(genome))

def reverse(seq):
	newseq = ""
	for i in range(len(seq)-1,-1,-1):
		if seq[i] == "A":
			newseq = newseq+"T"
		elif seq[i] == "T":
			newseq = newseq+"A"
		elif seq[i] == "C":
			newseq = newseq+"G"
		else:
			newseq = newseq + "C"
	return newseq
		

with open("ProteinTable167_161521.txt","r") as file:
	for line in file:
		if line[0] == "#":
		    #skip annotation header
			continue
		line = line.strip().split('\t')
		start = int(line[2])
		end = int(line[3])
		strand = line[4]
		if strand == "+":
		    #forward strand
			seq = genome[start-1:end]
		else:
		    #reverse strand
			seq = reverse(genome[start-1:end])
		
		#output locus tag and genome sequence separated by tab
		print line[7]+'\t'+seq



