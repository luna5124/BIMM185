from Bio import SwissProt
import gzip

file = gzip.open("uniprot_sprot_archaea.dat.gz",'rt')


ids = set() #set to store all the tax_ids that have been encountered
for seq_record in SwissProt.parse(file):
    
    #if the same tax_id has appeared before, used to remove duplicate
    if ','.join(seq_record.taxonomy_id) in ids:
        continue
    else:
        print(','.join(seq_record.taxonomy_id),seq_record.organism,','.join(seq_record.organism_classification),sep='\t')
        #print(seq_record.organism_classification)
        ids.add(','.join(seq_record.taxonomy_id))