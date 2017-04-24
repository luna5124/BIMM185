from Bio import SeqIO
import gzip
file = gzip.open('GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_protein.faa.gz','rt')

def print_function(s):
	print(s,end='\t')

for seq_record in SeqIO.parse(file,'fasta'):
	print_function(seq_record.id)
	print_function(seq_record.seq)
	print()



	#print(seq_record.seq)