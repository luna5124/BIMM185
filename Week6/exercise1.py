import sys
import pymysql
from scipy import stats
import numpy
import matplotlib.pyplot as plt

hostname = 'localhost'
username = 'root'
password = ''
database = 'bimm185'

def main():
	myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, local_infile=True, autocommit=True)
	count = 0

	gene_products = {}
	line_count = 0
	h0_file = open('h0.out','w')
	h1, h0 = [], []
	h1_file = open('h1.out','w')
	with open("GeneProductSet.txt",'r') as file:
		for line in file:
			line_count += 1
			if '#' in line:
				continue
			else:
				line = line.strip().split('\t')
				if len(line) < 3:
					continue
				#print(line_count, "length of line: " , len(line))
				gene_products[line[1]] = line[2]

	reverse = []
	forward = []
	directons = query_directons(myConnection)
	sorted_genes = []
	for d in directons:
		sorted_genes.append(d[0])
	#print(sorted_genes)

	with open('OperonSet.txt','r') as file:
		for line in file:
			if '#' in line:
				continue
			line = line.strip().split('\t')
			if len(line) != 8:
				continue
			gene_name = line[5]
			confidence = line[7]
			strand = line[3]
			if confidence == 'Strong' or confidence == 'Confirmed':
				count += 1
				gene_name = gene_name.split(',')
				#print(gene_name)
				if len(gene_name) < 2:
					continue
				pos = []
				genes = []
				for g in gene_name:
					gene_lefts = []
					gene_rights = []
					if "<" in g:
						#the gene name is malformed
						continue
					#print('hello')
					result = query_gene_name(myConnection, g)
					#print(g)
					if result is None:
						#print("Try finding the gene through synonym table: ", g)
						result = query_gene_synonym(myConnection, g)
					if result is None:
						if g in gene_products:
							locus_tag = gene_products[g]
							result = query_gene_locau_tag(myConnection, locus_tag)
							#if result is None:
								#print(g, 'locus tag: ', locus_tag, 'locus tag is not found in DB')
						#else:
							#print(g, 'not found in GeneProductSet')
					if result is not None:
						exons = query_exon(myConnection, result)
						for e in exons:
							gene_lefts.append(e[1])
							gene_rights.append(e[2])
						pos.append((min(gene_lefts), max(gene_rights)))
						genes.append(result)
						#print(g,min(gene_lefts),max(gene_rights),strand)

					
				pos.sort()
				#print(pos)
				'''
				if len(pos) == 0:
					continue
				if strand == 'forward':
					forward.append(pos)
				else:
					reverse.append(pos)
				'''

				for i in range(len(pos) - 1):
					h1.append(pos[i+1][0] - pos[i][1])
					h1_file.write(str(pos[i+1][0] - pos[i][1]) + '\n')

				if len(genes) == 0:
					continue
				print(genes)
				if strand == 'forward':
					#first gene is the leftmost
					if genes[0] in sorted_genes:
						gene_index = sorted_genes.index(genes[0])
						if gene_index != 0:

							prev = directons[gene_index - 1]
							#print(prev)
							if prev[2] == '+':
								distance = directons[gene_index][3] - prev[4]
								h0.append(distance)
								print(directons[gene_index],prev,distance)

					if genes[-1] in sorted_genes:
						gene_index = sorted_genes.index(genes[-1])
						if gene_index != len(sorted_genes) - 1:
							next_gene = directons[gene_index + 1]

							if next_gene[2] == "+":
								distance = next_gene[3] - directons[gene_index][4]
								h0.append(distance)
								print(directons[gene_index],next_gene,distance)


				else:

					if genes[0] in sorted_genes:
						gene_index = sorted_genes.index(genes[0])
						if gene_index != len(sorted_genes) - 1:

							next_gene = directons[gene_index + 1]

							if next_gene[2] == "-":
								distance = next_gene[3] - directons[gene_index][4]
								h0.append(distance)
								print(directons[gene_index],next_gene,distance)
						

					if genes[-1] in sorted_genes:
						gene_index = sorted_genes.index(genes[-1])
						if gene_index != 0:
							prev = directons[gene_index - 1]
							#print(prev)
							if prev[2] == '-':
								distance = directons[gene_index][3] - prev[4]
								h0.append(distance)
								print(directons[gene_index],prev,distance)
		#print(h0)
		for h in h0:
			h0_file.write(str(h) + '\n')

		#forward.sort()
		#reverse.sort()
		#print(forward)
		#PDF_calculate(h1)


		
	#density = stats.kde.gaussian_kde(h0)
	#plt.hist(density)
	#plt.show()
	h0_file.close()
	h1_file.close()
	#print(count)



def PDF_calculate(data):
	y = pdf(data,10)

def query_gene_synonym(conn, name):
	cur = conn.cursor()
	sql_statement = ("SELECT gene_id FROM gene_synonyms WHERE synonym = '{name}'".format(name=name))

	cur.execute(sql_statement)

	result = cur.fetchone()

	if result is None:
		return None
	else:
		return result[0]


def query_gene_name(conn, name):
	cur = conn.cursor()
	sql_statement = ("SELECT gene_id FROM genes WHERE name = '{name}';".format(name=name))
	#print(sql_statement)
	cur.execute(sql_statement)
	result = cur.fetchone()
	#print(result)
	if result is None:
		return None
	else:
		return result[0]
def query_gene_locau_tag(conn, locus_tag):
	cur = conn.cursor()
	sql_statement = ("SELECT gene_id FROM genes WHERE locus_tag = '{locus_tag}'".format(locus_tag=locus_tag))
	cur.execute(sql_statement)

	result = cur.fetchone()

	if result is None:
		return None
	else:
		return result[0]


def query_exon(conn, gene):
	cur = conn.cursor()
	sql_statement = ("SELECT gene_id, left_position, right_position FROM exons WHERE gene_id = '{gene}'".format(gene=gene))
	cur.execute(sql_statement)
	result = cur.fetchall()
	#print(gene)
	#print(result)
	return result

def query_directons(conn):
	cur = conn.cursor()
	sql_statement = ("select genes.gene_id, genes.name, strand, left_position, right_position from genes inner join(select gene_id, min(left_position) as left_position, max(right_position) as right_position from exons group by gene_id) position on position.gene_id = genes.gene_id where genes.genome_id = 1 order by left_position;")
	cur.execute(sql_statement)
	result = cur.fetchall()
	#print(result)
	return result


if __name__ == '__main__':
	main()

