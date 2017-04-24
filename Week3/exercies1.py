from Bio import SeqIO
import gzip


def print_function(s):
	print(s,end='\t')

file = gzip.open('GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.gbff.gz','rt')
#print(handle.read())
#my_input = handle.read()
#print(type(my_input))
#print(SeqIO.parse(handle,'genbank'))
print('accession','coordinates','strand','gene_name','locus_tag','synonyms','protein_name','Tax_ID','EC-numbers','external_references',sep='\t')

for seq_record in SeqIO.parse(file,'genbank'):
	#print("hey")
	#for f in seq_record.features:
	#	print("hello")
	#	print(f)
	#print(seq_record.id)
	#print(seq_record.name)
	#print(dir(seq_record))
	for f in seq_record.features:
		if f.type == "CDS":
			if 'protein_id' in f.qualifiers:
				#print(dir(f))
				#print(','.join(f.qualifiers['gene']),end='\t')
				#print(f.qualifiers.keys())
				print_function(','.join(f.qualifiers['protein_id']))
			elif 'pseudo' in f.qualifiers:
				#print(','.join(f.qualifiers['gene']),end='\t')
				print_function('pseudo')
			else:
				#print(','.join(f.qualifiers['gene']),end='\t')
				print_function('i don\'t know')

			print(f.location.start,f.location.end,sep='-',end='\t')
			if f.location.strand == 1:
				print_function('+')
			elif f.location.strand == -1:
				print_function('-')
			#print_function(f.location.strand)
			if 'gene' in f.qualifiers:
				print_function(','.join(f.qualifiers['gene']))
			else:
				print_function('-')

			if 'locus_tag' in f.qualifiers:
				print_function(','.join(f.qualifiers['locus_tag']))
			else:
				print_function('-')


			if 'gene_synonym' in f.qualifiers:
				print_function(','.join(f.qualifiers['gene_synonym']).replace('; ',','))
				#GSs = f.qualifiers['gene_synonym']
				#print(','.join(GSs),end='\t')
			else:
				print_function('-')

			if 'product' in f.qualifiers:
				print_function(','.join(f.qualifiers['product']))
			else:
				print_function('-')

			print_function(taxid)


			if 'EC_number' in f.qualifiers:
				#print(f.qualifiers['EC_number'],end='\t')
				print_function(','.join(f.qualifiers['EC_number']))
			else:
				print_function('-')

			if 'db_xref' in f.qualifiers:
				print_function(','.join(f.qualifiers['db_xref']))
			else:
				print_function('-')



			print()
		elif f.type == 'source':
			taxid = ','.join(f.qualifiers['db_xref']).replace('taxon:','')

			


file.close()
