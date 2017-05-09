import os

os.system('wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README')

protein_ids = []
with open('README') as file:
	for line in file:
		if "UP" in line:
			line = line.strip().split()
			protein_ids.append(line[0])
print(protein_ids)

wanted=['UP000034024', 'UP000050566','UP000000948']

ftp_address='ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/'

for w in wanted:
	os.system('wget -P {id} {ftp_address}{id}_*'.format(id=w,ftp_address=ftp_address))

