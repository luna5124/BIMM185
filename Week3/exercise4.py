from Bio import SwissProt
import gzip

file = gzip.open("uniprot_sprot_archaea.dat.gz",'rt')

print(type(file))

ids = set()
for seq_record in SwissProt.parse(file):
	#print("hello")
	#print(dir(seq_record))
	
	if ','.join(seq_record.taxonomy_id) in ids:
		continue
	else:
		print(','.join(seq_record.taxonomy_id),seq_record.organism,','.join(seq_record.organism_classification),sep='\t')
		ids.add(','.join(seq_record.taxonomy_id))
	#print(seq_record.organism)
	#print(seq_record.organism_classification)
