import sys
import pymysql
import scipy
from scipy import stats
import numpy
from numpy import linspace
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde
import math

hostname = 'localhost'
username = 'root'
password = ''
database = 'bimm185'

def main():
	myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, local_infile=True, autocommit=True)
	ecoli_dir = query_directons(myConnection, 1)
	genes = []
	out_file = open('conserved_gene_pairs.tab','w')
	for replicon in range(2,6):
		count = 0
		#get the orthologs between ecoli and current replicon
		result = query_orthologs(myConnection, replicon)
		ecoli_genes = []
		at_genes = []

		#store the gene_ids in list
		for r in result:
			at_genes.append(r[1])
			ecoli_genes.append(r[0])
		
		#get the directons of current replicon
		at_dir = query_directons(myConnection, replicon)

		#iterate through all the genes in ecoli which has an ortholog in the current replicon
		for i in range(len(ecoli_genes)):
			e = ecoli_genes[i]

			#get position of gene in ecoli
			index_ecoli = ecoli_dir.index((e,))

			#get position of the ortholog gene in at
			index_at = at_dir.index((at_genes[i],))
			
			#iterate through all genes within the range
			genes.append(e)
			for j in range(1,6):
				#get the paired gene
				if index_ecoli + j > len(ecoli_dir) - 1:
					#convert the coordiate to find the paired gene if necessary
					pair = ecoli_dir[(index_ecoli + j) - (len(ecoli_dir) - 1)][0]
				else:
					pair = ecoli_dir[index_ecoli+j][0]
				#if the paired gene also has an ortholog in the current at replicon
				if pair in ecoli_genes:
					
					#get the paired ortholog in current replicon
					pair_ecoli = ecoli_genes.index(pair)

					if (at_genes[pair_ecoli],) in at_dir:
						#get position of the paired ortholog
						pair_at = at_dir.index((at_genes[pair_ecoli],))
						
						#if the paired orthologs are also with max distance 5
						if abs(pair_at - index_at) <= 5:
							out_file.write(str(e) + '\t' + str(pair)+ '\t' + str(j) + '\t' + str(abs(pair_at - index_at)) + '\n')
							count += 1
		print("replicon: ", replicon, "count: ", count)
	out_file.close()



'''
This function was used to find the genes with the same name across e.coli and AT. 
Turns out we need to use orthologs.
This function was no longer used in the main function.
'''
def query_genes(conn, replicon):
	cur = conn.cursor()
	sql_statement = ("select t1.gene_id, t2.gene_id from (select * from genes where replicon_id = {replicon}) t1, (select * from genes where replicon_id = 1) t2 where t1.name = t2.name;".format(replicon=replicon))
	cur.execute(sql_statement)

	result = cur.fetchall()

	if result is None:
		return None
	else:
		return result


'''
This function gets all the directons of the given replicon
'''
def query_directons(conn, replicon):
	cur = conn.cursor()
	sql_statement = ("select genes.gene_id from genes inner join(select gene_id, min(left_position) as left_position, max(right_position) as right_position from exons group by gene_id) position on position.gene_id = genes.gene_id where genes.replicon_id = {replicon} order by left_position;".format(replicon=replicon))
	cur.execute(sql_statement)
	result = cur.fetchall()
	#print(result)
	return list(result)


'''
This functions gets all the ortholog gene pairs in E.coli and the given replicon
'''
def query_orthologs(conn, replicon):
	cur = conn.cursor()
	sql_statement = ("select * from orthologs where rid = {replicon}".format(replicon=replicon))
	cur.execute(sql_statement)
	result = cur.fetchall()
	return list(result)


'''
This function creats a temp view of orthologs between E.coli and AT.
The orthologs view was later used to query specific replicon orthologs.
'''
def construct_ortholog_temp_view(conn):
	cur = conn.cursor()

	#clear old view if exists
	cur.execute("drop view if exists orthologs;")

	#create new views
	sql_statement = ("create view orthologs as select g1.gene_id as qid, g2.gene_id as sid, g2.replicon_id as rid from (select b1max.qseqid as qseqid, b1max.sseqid as sseqid from "
					"(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_1 b, "
					"(select b1.qseqid,max(bitscore) as bitscore from blast_1 b1 group by b1.qseqid) maxtable "
					"where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b1max, "
					"(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_2 b, "
					"(select b2.qseqid,max(bitscore) as bitscore from blast_2 b2 group by b2.qseqid) maxtable "
					"where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b2max "
					"where b1max.qseqid = b2max.sseqid and b1max.sseqid = b2max.qseqid order by b1max.bitscore DESC) o1 inner join genes g1 on o1.qseqid = g1.accession inner join genes g2 on o1.sseqid = g2.accession;")

	cur.execute(sql_statement)


if __name__ == '__main__':
	main()
