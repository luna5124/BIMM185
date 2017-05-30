import sys
import pymysql
import scipy
from scipy import stats
import numpy
from numpy import linspace
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde

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
	operons = set()
	borders = set()
	border_dic = {}
	with open("../Week6/GeneProductSet.txt",'r') as file:
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

	with open('../Week6/OperonSet.txt','r') as file:
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
						if g in gene_products:
							locus_tag = gene_products[g]
							result = query_gene_locau_tag(myConnection, locus_tag)

					if result is None:
						#print("Try finding the gene through synonym table: ", g)
						result = query_gene_synonym(myConnection, g)
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
				print(genes)

				for i in range(len(pos) - 1):
					#print(genes[i],genes[i+1])
					h1.append(pos[i+1][0] - pos[i][1])
					h1_file.write(str(pos[i+1][0] - pos[i][1]) + '\n')

				if len(genes) == 0:
					continue
				
				#print("start calculate h0")

				if strand == 'forward':
					#first gene is the leftmost
					for i in range(len(genes)-1):
						operons.add((genes[i],genes[i+1]))

					if genes[0] in sorted_genes:
						gene_index = sorted_genes.index(genes[0])
						
						if gene_index != 0:

							prev = directons[gene_index - 1]

							#print(prev)
							if prev[0] not in border_dic:
								if prev[2] == '+':
									distance = directons[gene_index][3] - prev[4]
									borders.add((prev[0],genes[0]))
									h0.append(distance)
									border_dic[prev[0]] = genes[0]
									border_dic[genes[0]] = prev[0]
									print(prev[0],genes[0])
								else:
									print(prev[0],genes[0],'not on the same strand')
							elif border_dic[prev[0]] != genes[0]:
								if prev[2] == '+':
									distance = directons[gene_index][3] - prev[4]
									borders.add((prev[0],genes[0]))
									h0.append(distance)
									border_dic[prev[0]] = genes[0]
									border_dic[genes[0]] = prev[0]
									print(prev[0],genes[0])
								else:
									print(prev[0],genes[0],'not on the same strand')

								#print(directons[gene_index],prev,distance)

					if genes[-1] in sorted_genes:
						gene_index = sorted_genes.index(genes[-1])
						if gene_index != len(sorted_genes) - 1:
							next_gene = directons[gene_index + 1]
							borders.add((genes[-1],next_gene[0]))
							if next_gene[0] not in border_dic:
								if next_gene[2] == "+":
									distance = next_gene[3] - directons[gene_index][4]
									h0.append(distance)
									border_dic[next_gene[0]] = genes[-1]
									border_dic[genes[-1]] = next_gene[0]
									print(next_gene[0],genes[-1])
								else:
									print(next_gene[0],genes[-1], 'not on the same strand')
							elif border_dic[next_gene[0]] != genes[-1]:
								if next_gene[2] == "+":
									distance = next_gene[3] - directons[gene_index][4]
									h0.append(distance)
									border_dic[next_gene[0]] = genes[-1]
									border_dic[genes[-1]] = next_gene[0]
									print(next_gene[0],genes[-1])
								else:
									print(next_gene[0],genes[-1],'not on the same strand')
								#print(directons[gene_index],next_gene,distance)


				else:
					for i in range(len(genes)-1,-1,-1):
						operons.add((genes[i],genes[i-1]))

					if genes[0] in sorted_genes:
						gene_index = sorted_genes.index(genes[0])
						if gene_index != len(sorted_genes) - 1:

							next_gene = directons[gene_index + 1]
							borders.add((genes[0],next_gene[0]))
							if next_gene[0] not in border_dic:
								if next_gene[2] == "-":
									distance = next_gene[3] - directons[gene_index][4]
									h0.append(distance)
									border_dic[next_gene[0]] = genes[-1]
									border_dic[genes[-1]] = next_gene[0]
									print(next_gene[0],genes[-1])
								else:
									print(next_gene[0],genes[-1],'not on the same strand')
							elif border_dic[next_gene[0]] != genes[-1]:
								if next_gene[2] == "-":
									distance = next_gene[3] - directons[gene_index][4]
									h0.append(distance)
									border_dic[next_gene[0]] = genes[-1]
									border_dic[genes[-1]] = next_gene[0]
									print(next_gene[0],genes[-1])
								else:
									print(next_gene[0],genes[-1],'not on the same strand')

								#print(directons[gene_index],next_gene,distance)
						

					if genes[-1] in sorted_genes:
						gene_index = sorted_genes.index(genes[-1])
						if gene_index != 0:
							prev = directons[gene_index - 1]
							borders.add((prev[0],genes[-1]))
							#print(prev)
							if prev[0] not in border_dic:
								if prev[2] == '-':
									distance = directons[gene_index][3] - prev[4]
									h0.append(distance)
									border_dic[prev[0]] = genes[0]
									border_dic[genes[0]] = prev[0]
									print(prev[0],genes[0])
								else:
									print(prev[0],genes[0],'not on the same strand')
							elif border_dic[prev[0]] != genes[-1]:
								if prev[2] == '-':
									distance = directons[gene_index][3] - prev[4]
									h0.append(distance)
									border_dic[prev[0]] = genes[0]
									border_dic[genes[0]] = prev[0]
									print(prev[0],genes[0])
								else:
									print(prev[0],genes[0],'not on the same strand')


									#print(directons[gene_index],prev,distance)
		#print(h0)

		for h in h0:
			h0_file.write(str(h) + '\n')
	print("operon count: ", count)
	h0_file.close()
	h1_file.close()
	#print("border_dic: ", border_dic)
	#print(operons)
	#posteria_calculate(h0, h1, sorted_genes, directons, operons,borders)
	#create_tu(myConnection)
	#import_tu(myConnection)
	#print("operon count:", count)

	kde0, kde1 = pdf_calculate(h0, h1)

	for replicon in range(2,6):
		sorted_genes_AT = []
		directons_AT = query_directions_AT(myConnection,replicon)
		posteria_calculate(h0, h1, sorted_genes_AT, directions_AT, operons, borders)


def posteria_calculate(h0, h1, sorted_genes, directons, operons,borders):
	kde0, kde1 = pdf_calculate(h0, h1)
	posts = []
	distances = []
	directon = []
	direction = ""
	predict_file=open('predict.tab','w')
	for d in directons:
		if direction == "":
			directon.append((d[0],d[3],d[4]))
			direction = d[2]
			continue
		elif direction == d[2]:
			directon.append((d[0],d[3],d[4]))
		else:
			print(directon)
			if len(directon) <= 1:
				directon = [(d[0],d[3],d[4])]
				direction = d[2]
				continue
			for i in range(len(directon)-1):
				distance = directon[i+1][1] - directon[i][2]
				pair = (directon[i][0],directon[i+1][0])
				predict_file.write(str(pair[0])+'\t'+str(pair[1])+'\t' + str(distance) + '\t')
				if pair in operons:
					#print(directon[i][0],directon[i+1][0], 'this pair in operon')
					predict_file.write('TP'+'\t')
				elif pair in borders:
					#print(directon[i][0],directon[i+1][0], 'this pair not in operon')
					predict_file.write('TN'+'\t')
				else:
					predict_file.write('UNDETERMINED'+'\t')
				if kde1(distance) * 0.6 == 0:
					posts.append(0)
					predict_file.write('0'+'\n')
				else:
					pos = kde1(distance) * 0.6 / (kde1(distance) * 0.6 + kde0(distance) * 0.4)
					posts.append(pos[0])
					predict_file.write(str(pos[0])+'\n')
				
				'''
				for j in range(i+1, len(directon)):
					distance = directon[j][0] - directon[i][1]
					#print(distance,kde1(distance),kde0(distance))
					if kde1(distance) * 0.6 == 0:
						posts.append(0)
					else:
						pos = kde1(distance) * 0.6 / (kde1(distance) * 0.6 + kde0(distance) * 0.4)
						posts.append(pos[0])
				'''
					

				distances.append(distance)

			directon = [(d[0],d[3],d[4])]
			direction = d[2]
	predict_file.close()
	#print(distances, posts)
	prob_to_plot = []
	dist_to_plot = [i for i in range(-200,600)]
	for i in range(-200, 600):
		prob_to_plot.append(kde1(i) * 0.5 / (kde1(i) * 0.5 + kde0(i) * 0.5))
	plt.plot(dist_to_plot, prob_to_plot,'y.')
	plt.xlim([-200,600])
	#plt.show()
	


def pdf_calculate(h0, h1):
	dist_space0 = linspace(-200, 2000, 1000)

	kde1 = gaussian_kde(h1, 0.5)
	kde1.covariance_factor = lambda : 0.25
	kde1._compute_covariance()


	density1 = kde1(dist_space0)
	max_density1 = max(density1)
	for i in range(len(density1)):
		density1[i] = density1[i]/max_density1
	plt.plot(dist_space0, kde1(dist_space0)/max(kde1(dist_space0)))

	kde0 = gaussian_kde(h0,0.5)
	kde0.covariance_factor = lambda : 0.25
	kde0._compute_covariance()
	
	density0 = kde0(dist_space0)
	#max_density0 = max(density0)
	dist0 = [i for i in range(min(h0),min(h0))]
	for i in range(len(density0)):
		density0[i] = density0[i]/max_density1
		#print(max_density0)
	plt.plot(dist_space0, kde0(dist_space0)/max(kde1(dist_space0)))
	
	#print("max density0: ", max_density0)
	#print(density0)


	#print(kde0(0))
	#print(kde0(1))
	#print(kde1(0))
	#print(kde1(1))

	#plt.show()
	return kde0, kde1

def query_gene_synonym(conn, name):
	cur = conn.cursor()
	sql_statement = ("SELECT gene_id FROM gene_synonyms WHERE synonym = '{name}'".format(name=name))

	cur.execute(sql_statement)

	result = cur.fetchone()

	if result is None:
		return None
	else:
		return result[0]


def create_tu(conn):
	cur = conn.cursor()
	sql_statement = ("DROP TABLE IF EXISTS tus;\n"
	"CREATE TABLE tus(\n"
  	"gid_1 INT (10) UNSIGNED NOT NULL,\n"
  	"gid_2 INT (10) UNSIGNED NOT NULL,\n"
  	"distance INT  (10) NOT NULL,\n"
  	"status ENUM('TP', 'TN', 'UNDETERMINED') NOT NULL,\n"
  	"prob DOUBLE NOT NULL,\n"
  	"KEY (gid_1),\n"
  	"KEY (gid_2)\n"
	")ENGINE=InnoDB;")
	#print(sql_statement)
	cur.execute(sql_statement)

def import_tu(conn):
	cur = conn.cursor()
	sql_statement = ("LOAD DATA LOCAL INFILE 'predict.tab' INTO TABLE tus;")
	cur.execute(sql_statement)

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

def query_directions_AT(conn, replicon):
	cur = conn.cursor()
	sql_statement = ("select genes.gene_id, genes.name, strand, left_position, right_position from genes inner join(select gene_id, min(left_position) as left_position, max(right_position) as right_position from exons group by gene_id) position on position.gene_id = genes.gene_id where genes.replicon_id = {replicon} order by left_position;".format(replicon=replicon))
	cur.execute(sql_statement)
	result = cur.fetchall()
	#print(result)
	return result

if __name__ == '__main__':
	main()

