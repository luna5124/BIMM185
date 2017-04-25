import os


'''
import subprocess
subprocess.Popen("cwm --rdf test.rdf --ntriples > test.nt")
'''

samples = []
with open('E.coli.K12.txt','r') as file:
	for line in file:
		line = line.strip().split('\t')
		tax_id = line[0]
		name = line[1]
		name = name.replace(" ", "_")
		print(name)
		name += "_"+tax_id
		ftp = line[2]
		ftp = ftp.replace("ftp","rsync")
		print(ftp)
		samples.append((name,ftp))

for s in samples:
	#print('rsync -avzL {ftp} {name}'.format(ftp=s[1],name=s[0]))
	os.system('rsync -avzL {ftp} ./genome'.format(ftp=s[1]))
