#Read in the whole genome reference
genome = ""
with open("GCF_000005845.2_ASM584v2_genomic.fna",'r') as file:
	file.readline()
	for line in file:
		line = line.strip()
		genome = genome + line


#Function used to produce the reverse compliment of a gene when the protein is on the reverse strand
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
		
#Read the gene annotation file
with open("ProteinTable167_161521.txt","r") as file:
	for line in file:
	    #skip the header line
		if line[0] == "#":
			continue
		line = line.strip().split('\t')
		start = int(line[2])
		end = int(line[3])
		strand = line[4]
		print(">" + line[8]+"|"+line[6]+"|"+line[7])
		
		
		if strand == "+":
		    #forward strand
			seq = genome[start-1:end]
			
		else:
		    #forward strand
		    #Take reverse compliment of the genes
			seq = reverse(genome[start-1:end])
		
		#Print the genome sequence in segments of 70 nucleotides
		for i in range(0,len(seq),70):
            print(seq[i:i+70])