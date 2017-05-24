import sys
import pymysql
import matplotlib.pyplot as plt
import numpy as np

hostname = 'localhost'
username = 'root'
password = ''
database = 'bimm185'
	

def query_avg(conn):
	cur = conn.cursor()
	sql_statement = ("select avg(prob) from tus where status = 'TP';")
	cur.execute(sql_statement)
	result = cur.fetchone()
	return result

def query_min(conn):
	cur = conn.cursor()
	sql_statement = ("select min(prob) from tus where status = 'TP';")
	cur.execute(sql_statement)
	result = cur.fetchone()
	return result

def query_max(conn):
	cur = conn.cursor()
	sql_statement = ("select max(prob) from tus where status = 'TP';")
	cur.execute(sql_statement)
	result = cur.fetchone()
	return result


def query_count(conn):
	cur = conn.cursor()
	sql_statement = ("select count(*), status from tus group by status;")
	cur.execute(sql_statement)
	result = cur.fetchall()

	return result


def query_prob(conn, threshold):
	cur = conn.cursor()
	sql_statement = ("select count(*), status from tus where prob > {threshold} group by status;".format(threshold=threshold))
	cur.execute(sql_statement)
	result = cur.fetchall()
	#print(gene)
	#print(result)
	return result


def main():
	myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, local_infile=True, autocommit=True)

	prob_avg = query_avg(myConnection)[0]
	prob_min = query_min(myConnection)[0]
	prob_max = query_max(myConnection)[0]

	count_result = query_count(myConnection)
	tp = count_result[0][0]
	tn = count_result[1][0]

	for i in np.arange(prob_min, prob_max, 0.01):
		#print(i)
		result = query_prob(myConnection, i)
		tp_count = result[0][0]
		fp_count = result[1][0]
		sensitivity = tp_count / tp
		specificity = (tn - fp_count) / tn
		accuracy = (tp_count + tn - fp_count)/ (tp + tn)
		print(i, sensitivity, specificity, 1-specificity, accuracy, sep='\t')







if __name__ == '__main__':
	main()