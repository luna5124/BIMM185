import sys
import pymysql

hostname = 'localhost'
username = 'root'
password = ''
database = 'bimm185'

def main():
	myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, local_infile=True, autocommit=True)

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
				#print(gene_name)
				gene_name = gene_name.split(',')
				for g in gene_name:
					#print('hello')
					print(query_gene_name(myConnection, g))



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

if __name__ == '__main__':
	main()
