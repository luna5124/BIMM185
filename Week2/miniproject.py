import textwrap
import matplotlib.pyplot as plt
import numpy as np

#Use the the listed order of codon in the output
codon_list = ["ATT", "ATC", "ATA","CTT", "CTC", "CTA", "CTG", "TTA", "TTG","GTT", "GTC", "GTA", "GTG","TTT", "TTC","ATG","TGT", "TGC","GCT", "GCC", "GCA", "GCG","GGT", "GGC", "GGA", "GGG","CCT", "CCC", "CCA", "CCG","ACT", "ACC", "ACA", "ACG","TCT", "TCC", "TCA", "TCG", "AGT", "AGC","TAT", "TAC","TGG","CAA", "CAG","AAT", "AAC","CAT", "CAC","GAA", "GAG","GAT", "GAC","AAA", "AAG","CGT", "CGC", "CGA", "CGG", "AGA", "AGG","TAA", "TAG", "TGA"]

#Output header
print ("Gene",end='\t')
for c in codon_list:
        print (c,end='\t')
print ("Length")


counts = {}
freqs = []
genes = []
readfile = open("exercise2_modified.txt",'r')
gene_prob = open("gene_prob.txt",'w')
for line in readfile:
        freq = [0] * 64
        line = line.strip().split('\t')
        gene = line[0]
        genes.append(gene)
        #Separated genome sequence into segments of 3 nucleotides(codons)
        codons = textwrap.wrap(line[1],3)
        print (gene,end='\t')
        #Count occurrences of each codon in order
        for i in range(len(codon_list)):
                c = codon_list[i]
                #print(codons)
                print(codons.count(c),end='\t')
                #increment global codon occurrences and store in a dictionary
                if c in counts:
                        counts[c] += codons.count(c)
                else:
                        counts[c] = codons.count(c)
                #calculate relative frequencies for each codon
                freq[i] = float(codons.count(c)/(len(line[1])/3))
        #store the frequencies in the matrix
        freqs.append(freq)
        
        #output total codon count of each gene
        print(len(line[1])/3,end='\t')
        
        #if the length of the gene is not multiply of 3, output warning message
        if len(line[1]) % 3 != 0:
                print ("Seq length not multiply of 3")
        else:
                print()

#Output the global occurrences of each codon
print("Totals",end='\t')
for c in codon_list:
        print(counts[c],end="\t")
print(sum(counts.values()))

#Calculate CUIs
total_CUI = 0
CUIS = []
for i in range(len(genes)):
        #iterate through each gene
        CUI = 0
        for j in range(len(codon_list)):
                c = codon_list[j]
                CUI += freqs[i][j] * counts[c]/sum(counts.values())
        total_CUI += CUI
        CUIS.append(CUI)
        gene_prob.write(genes[i] + "\t" + str(CUI) + "\n")

#Plot the histogram
binwidth = 0.0001
plt.hist(CUIS, bins=np.arange(min(CUIS), max(CUIS) + binwidth, binwidth))
plt.savefig("count_hist.png")