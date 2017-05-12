import sys
import pymysql

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
				for g in gene_name:
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
						gene_lefts = []
						gene_rights = []
						for e in exons:
							gene_lefts.append(e[1])
							gene_rights.append(e[2])
						pos.append((min(gene_lefts), max(gene_rights)))
					
				pos.sort()
				#print(pos)
				if len(pos) == 0:
					continue
				if strand == 'forward':
					forward.append(pos)
				else:
					reverse.append(pos)

				for i in range(len(pos) - 1):
					h1_file.write(str(pos[i+1][0] - pos[i][1]) + '\n')

		forward.sort()
		reverse.sort()
		#print(forward)

		for i in range(len(forward) - 1):
			h0_file.write(str(forward[i+1][0][0] - forward[i][-1][-1]) + '\n')
		for i in range(len(reverse) - 1):
			#print(reverse[i],reverse[i][-1][-1], reverse[i+1], reverse[i+1][0][0])
			h0_file.write(str(reverse[i+1][0][0] - reverse[i][-1][-1]) + '\n')

		print(query_directons(myConnection))
	#print(count)





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
	sql_statement = ("select genes.gene_id, strand, left_position, right_position from genes inner join(select gene_id, min(left_position) as left_position, max(right_position) as right_position from exons group by gene_id) position on position.gene_id = genes.gene_id order by left_position;")
	cur.execute(sql_statement)
	result = cur.fetchall()
	print(result)


if __name__ == '__main__':
	main()

