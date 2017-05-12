import sys
import pymysql

hostname = 'localhost'
username = 'root'
password = ''
database = 'bimm185'

def main():
	myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, local_infile=True, autocommit=True)
	count = 0
	with open('TUSet.txt','r') as file:
		for line in file:
			if '#' in line:
				continue
			line = line.strip().split('\t')
			if len(line) != 7:
				continue
			gene_name = line[3]
			confidence = line[6]
			if confidence == 'Strong' or confidence == 'Confirmed':
				count += 1
				print(gene_name)
				gene_name = gene_name.split(',')
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
						print("Try finding the gene through synonym table: ", g)
						result = query_gene_synonym(myConnection, g)

					if result is not None:
						exons = query_exon(myConnection, result)
						gene_lefts = []
						gene_rights = []
						for e in exons:
							gene_lefts.append(e[1])
							gene_rights.append(e[2])
						pos.append((min(gene_lefts), max(gene_rights)))
				pos.sort()
				print(pos)
	print(count)





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

def query_exon(conn, gene):
	cur = conn.cursor()
	sql_statement = ("SELECT gene_id, left_position, right_position FROM exons WHERE gene_id = '{gene}'".format(gene=gene))
	cur.execute(sql_statement)
	result = cur.fetchall()
	#print(gene)
	#print(result)
	return result


if __name__ == '__main__':
	main()
