from Bio import SeqIO
import gzip
import sys
import os
import pymysql

hostname = 'localhost'
username = 'root'
password = ''
database = 'bimm185'

def read_blast_result(files):
	#out_file = open(f+'_blast_result_parsed.tab','w')
	for f in files:
		file = open(f,'r')
		out_file = open(f+'_blast_result_parsed.tab','w')
		for line in file:
			line = line.strip().split('\t')
			#print(line)
			#qseqid, sseqid, qlen, slen, bitscore, evalue, pident, nident, length, qcovs, qstat, qend, sstart, send
			
			#calculate scov = length/slen
			scov = int(float(line[8])/float(line[3]) * 100)
			line[0] = line[0].split('.')[0]
			line[1] = line[1][4:len(line[1])-2].split('.')[0]
			#print(line)
			line.append(str(scov))
			#print(line)
			out_file.write('\t'.join(line)+'\n')
		file.close()
		out_file.close()




def query_genome_id(conn, tax_id):
	cur = conn.cursor()
	sql_statement = ("SELECT genome_id FROM genomes WHERE tax_id = {tax_id};".format(tax_id=tax_id))
	cur.execute(sql_statement)
	result = cur.fetchone()
	if result[0] is None:
		return 0
	else:
		return result[0]


def create_new_table(conn,genome):
	#WP_000904906	NP_415676	204	184	146	1.15e-45	54.375	87	160	78	1	160	1	151	0.8695652173913043
	cur = conn.cursor()
	cur.execute("DROP TABLE IF EXISTS blast_{genome_id};".format(genome_id=genome))
	sql_statement = ("CREATE TABLE blast_{genome_id}(\n"
		"qseqid VARCHAR (100) NOT NULL,\n"
		"sseqid VARCHAR (100) NOT NULL,\n"
		"qlen INT (10) UNSIGNED NOT NULL,\n"
		"slen INT (10) UNSIGNED NOT NULL,\n"
		"bitscore DOUBLE NOT NULL,\n"
		"evalue DOUBLE NOT NULL,\n"
		"pident DOUBLE NOT NULL,\n"
		"nident INT (10) UNSIGNED NOT NULL,\n"
		"length INT (10) UNSIGNED NOT NULL,\n"
		"qcovs INT (10) UNSIGNED NOT NULL,\n"
		"qstart INT (10) UNSIGNED NOT NULL,\n" 
		"qend INT (10) UNSIGNED NOT NULL,\n"
		"sstart INT (10) UNSIGNED NOT NULL,\n"
		"send INT (10) UNSIGNED NOT NULL,\n"
		"scov INT (10) UNSIGNED NOT NULL,\n"
		"KEY (qseqid, sseqid)\n"
		")ENGINE=InnoDB;".format(genome_id=genome))
	#print(sql_statement)
	cur.execute(sql_statement)
	cur.close()


def load_blast_result(conn, out_file, genome):
	cur = conn.cursor()
	sql_statement = ("LOAD DATA LOCAL INFILE '{out_file}' INTO TABLE blast_{genome_id}"
		"(qseqid, sseqid, qlen, slen, bitscore, evalue, pident, nident, length, qcovs, qstart, qend, sstart, send, scov);"
		.format(out_file=out_file, genome_id=genome))
	cur.execute(sql_statement)
	cur.close()





def main():
    #os.system('mysql -u root -p bimm185 < create_tables.sql')
	myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, local_infile=True, autocommit=True)
	read_blast_result(['E_coli_k12_vs_A.tumefaciens.out','A.tumefaciens_vs_E_coli_k12.out'])
	create_new_table(myConnection,1)
	load_blast_result(myConnection,'E_coli_k12_vs_A.tumefaciens.out_blast_result_parsed.tab',1)
	create_new_table(myConnection,2)
	print('load E.coli blast results')
	load_blast_result(myConnection,'A.tumefaciens_vs_E_coli_k12.out_blast_result_parsed.tab',2)
	print('load A.tumefaciens blast results')
    #mx_genome_id = query_mx_genome_id(myConnection)

    #print("in main: ", mx_genome_id)
    #mx_replicon_id = query_mx_replicon_id(myConnection)
    #mx_gene_id = query_mx_replicon_id(myConnection)

    #input_files = sys.argv[1:]

	myConnection.close()




if __name__ == '__main__':
	main()