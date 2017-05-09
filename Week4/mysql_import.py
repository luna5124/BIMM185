from Bio import SeqIO
import gzip
import sys
import os
import pymysql

hostname = 'localhost'
username = 'root'
password = ''
database = 'bimm185'
#mysqldb usage from stackoverflow
#http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python


'''
genome.tab format:accession,genome_short_name,genome_long_name,domain,size,release_date,tax_id
'''

'''
replicon.tab format:
genome_id
name
rep_size
type
structure
num_genes
'''

'''
genes.tab format:
gene_id
genome_id
replicon_id
strand
name
locus_tab
number of exons
length
product name
'''

'''
exons.tab format:
gene_id
left
right
size

'''



def read_genbank(input_files, myConnection):
    #open output files
    genome_file = open('genomes.tab','w')
    replicon_file = open('replicons.tab','w')
    gene_file = open('genes.tab','w')
    exon_file = open('exons.tab','w')
    synonym_file = open('gene_synonyms.tab','w')
    reference_file=open('ex_references.tab','w')
    function_file=open('functions.tab','w')
    

    #set counter
    #genome_count = mx_genome_id
    #replicon_count = mx_replicon_id
    gene_count = query_mx_gene_id(myConnection)
    replicon_count = query_mx_replicon_id(myConnection)

    for input_file in input_files:
        #genome_count += 1
        cds_count = 0

        file = gzip.open(input_file,'rt')
        inserted_genome = False

        #print header
        #print('#accession','coordinates','strand','gene_name','locus_tag','synonyms','protein_name','Tax_ID','EC-numbers','external_references',sep='\t')
        #iterate through all the records in the input

        for seq_record in SeqIO.parse(file,'genbank'):
            #print(seq_record.dbxrefs)
            replicon_count += 1
            taxid = ','.join(seq_record.features[0].qualifiers['db_xref']).replace('taxon:','')
            if not inserted_genome:
                #insert new genome into DB
                long_name = seq_record.annotations['source']
                short_name = '_'.join(long_name.split()[:2])
                domain = 'bacteria'
                length = str(len(seq_record.seq))
                date = seq_record.annotations['date']
                insert_genomes_table(myConnection, short_name, long_name, domain, length, date,taxid)
                genome_count = query_mx_genome_id(myConnection)
                inserted_genome = True

            cds_count = 0

            #replicon_count += 1
            #seq_record = parses[j]
            #print('#',seq_record.id)
            #genome_file.write(seq_record.annotations['topology']+'\t')
            
            #write genome.tab

            #write replicon.tab
            '''
            replicon_file.write(str(genome_count)+'\t')
            replicon_file.write(seq_record.description+'\t')
            replicon_file.write(str(len(seq_record.seq))+'\t')

            
            if 'chromosome' in seq_record.description:
                replicon_file.write('chromosome\t')
            elif 'plasmid' in seq_record.description:
                replicon_file.write('plasmid\t')
            else:
                replicon_file.write('unknown\t')

            replicon_file.write(seq_record.annotations['topology']+'\t')
            '''
            #insert new replicon into DB
            #genome_id, name, rep_size, type, structure, num_genes, accession
            #insert_replicons_table(myConnection, genome_id, name, rep_size, replicon_type, replicon_structure, accession)
            #replicon_count = query_mx_replicon_id(myConnection)

            #gene_count = 0
            for f in seq_record.features:
                #check if it is CDS
                if f.type == "CDS":
                    gene_count += 1
                    #gene_count += 1
                    cds_count += 1
                    #check if it has protein_id

                    #insert new gene into db
                    #accession, genome_id, replicon_id, strand, name, locus_tag, num_exons, size, product


                    if 'protein_id' in f.qualifiers:
                        protein_id = ','.join(f.qualifiers['protein_id']).split('.')[0]

                        #gene_file.write(','.join(f.qualifiers['protein_id'])+'\t')
                    elif 'pseudo' in f.qualifiers:
                        #print(','.join(f.qualifiers['gene']),end='\t')
                        protein_id = 'pseudo'
                        
                        #gene_file.write('pseudo\t')
                    else:
                        #print(','.join(f.qualifiers['gene']),end='\t')
                        protein_id = 'i don\'t know\t'
                        #gene_file.write('i don\'t know\t')

                    #gene_file.write(accession + '\t')
                    #gene_file.write(str(genome_count)+'\t')
                    #gene_file.write(str(replicon_count)+'\t')
                    #get location
                    #print(f.location.start,f.location.end,sep='-',end='\t')
                    
                    #forward strand = 1, reverse strand = -1
                   
                    if f.location.strand == 1:
                        strand = '+'
                    elif f.location.strand == -1:
                        strand = '-'
                    
                    #print gene name
                    if 'gene' in f.qualifiers:
                        gene_name = ','.join(f.qualifiers['gene'])
                    else:
                        gene_name = '-'

                    #print locus tag
                    if 'locus_tag' in f.qualifiers:
                        locus_tag = ','.join(f.qualifiers['locus_tag'])
                    else:
                        locus_tag = '-'

                    exon_count = str(len(f.location.parts))
                    gene_length = str(len(f.location))

                    if 'product' in f.qualifiers:
                        gene_product = ','.join(f.qualifiers['product'])
                    else:
                        gene_product = '-'

                    gene_file.write('\t'.join([str(gene_count), protein_id, str(genome_count), str(replicon_count), strand, gene_name, locus_tag, exon_count, gene_length, gene_product]))
                    #insert_genes_table(myConnection, protein_id, genome_count, replicon_count, strand, gene_name, locus_tag, exon_count, gene_length, gene_product)
                    #gene_count = query_mx_gene_id(myConnection)
                    

                    #print synonym
                    #synonym_file.write(str(gene_count)+'\t')
                    if 'gene_synonym' in f.qualifiers:
                        #synonym_file.write(str(gene_count)+'\t')
                        synonyms = '; '.join(f.qualifiers['gene_synonym'])
                        synonyms = synonyms.split('; ')
                        #print(synonyms)
                        #print(f.qualifiers['gene_synonym'][0]).split()
                        for s in synonyms:
                            #print(s)
                            synonym_file.write(str(gene_count)+'\t')
                            synonym_file.write(s+'\n')

                        #synonym_file.write(','.join(f.qualifiers['gene_synonym']).replace('; ',',')+'\n')
                        #GSs = f.qualifiers['gene_synonym']
                        #print(','.join(GSs),end='\t')
                    #else:
                    #    synonym_file.write('-\n')
                    

                    for e in f.location.parts:
                        #insert_exons_table(myConnection, gene_count, str(int(e.start)),str(int(e.end)),str(len(e)))
                        
                        exon_file.write(str(gene_count)+'\t')
                        exon_file.write(str(int(e.start)) + '\t')
                        exon_file.write(str(int(e.end)) + '\t')
                        exon_file.write(str(len(e))+'\n')

                    '''
                    print(f.location)
                    print(dir(f.location))
                    for e in f.location.parts:
                        print(e)
                    gene_file.write(str(len(f.location))+'\t')
                    print(len(f.location))
                    gene_file.write(str(int(f.location[-1].end) - int(f.location[0].start)) + '\t')
                    '''
                    #print product name

                    #else:
                    #    gene_file.write('-\t')

                    #gene_file.write(taxid+'\t')
                    
                    if 'function' in f.qualifiers:
                        function_file.write(str(gene_count) + '\t')
                        #for function in f.qualifiers['function']:
                        #    function_file.write(str(gene_count) + '\t')
                        #    function_file.write(function+'\n')

                        function_file.write(','.join(f.qualifiers['function']) + '\n')
                    #print EC_number
                    '''
                    if 'EC_number' in f.qualifiers:
                        gene_file.write(','.join(f.qualifiers['EC_number']))
                    else:
                        gene_file.write('-')
                    '''
                    #print external references

                    #reference_file.write(str(gene_count)+'\t')
                    if 'db_xref' in f.qualifiers:
                        for xref in f.qualifiers['db_xref']:
                            reference_file.write(str(gene_count) + '\t')
                            reference_file.write('\t'.join(xref.split(':'))+'\n')
                            #print(xref)
                        #_file.write(','.join(f.qualifiers['db_xref']))
                    #else:
                    #    reference_file.write(str(gene_count) + '\t')
                    #    reference_file.write('-\t-\n')
                    
        
                    #change new line

                    gene_file.write('\n')
                #obtain taxid from source line
                elif f.type == 'source':
                    taxid = ','.join(f.qualifiers['db_xref']).replace('taxon:','')

            genome_id = str(genome_count)
            name = seq_record.description
            rep_size = str(len(seq_record.seq))
            if 'chromosome' in seq_record.description:
                replicon_type = 'chromosome'
            elif 'plasmid' in seq_record.description:
                replicon_type = 'plasmid'
            else:
                replicon_type = 'unknown'
            replicon_structure = seq_record.annotations['topology']
            accession = seq_record.name
            replicon_file.write('\t'.join([str(genome_id), name, rep_size, replicon_type, replicon_structure, str(cds_count),accession])+'\n')
            #update_replicon_gene_count(myConnection, replicon_count, cds_count)
            #replicon_file.write(str(cds_count)+'\t')
            #replicon_file.write(seq_record.name+'\n')

            
        file.close()
    genome_file.close()
    replicon_file.close() 
    #genome_file = open('genomes.tab','w')
    #replicon_file = open('replicons.tab','w')
    gene_file.close()
    exon_file.close()
    synonym_file.close()
    reference_file.close()
    function_file.close()


# Simple routine to run a query on a database and print the results:
def query_mx_genome_id(conn):
    cur = conn.cursor()
    cur.execute("SELECT max(genome_id) FROM genomes;")
    result = cur.fetchone()
    cur.close()

    if result[0] is None:
        return 0
    else:
        return result[0]
        
def query_mx_replicon_id(conn):
    cur = conn.cursor()

    cur.execute("SELECT max(replicon_id) FROM replicons;")

    result = cur.fetchone()
    cur.close()
    if result[0] is None:
        return 0
    else:
        return result[0]

def query_mx_gene_id(conn):
    cur = conn.cursor()

    cur.execute("SELECT max(gene_id) FROM genes;")

    result = cur.fetchone()
    cur.close()
    if result[0] is None:
        return 0
    else:
        return result[0]

def insert_genomes_table(conn,genome_short_name, genome_long_name, domain, size, release_date, tax_id):
    cur = conn.cursor()

    sql_statement = ("INSERT INTO genomes(genome_short_name,genome_long_name,domain,size,release_date,tax_id) "
        "VALUES ('{genome_short_name}','{genome_long_name}','{domain}','{size}','{release_date}','{tax_id}');"
        .format(genome_short_name=genome_short_name, genome_long_name=genome_long_name, domain=domain, size=size, release_date=release_date, tax_id=tax_id))

    #print(sql_statement)
    cur.execute(sql_statement)
    #print("finish insert gene", genome_short_name)
    cur.close()


def insert_replicons_table(conn, genome_id, name, rep_size, replicon_type, structure, accession):
    cur = conn.cursor()

    sql_statement = ("INSERT INTO replicons(genome_id, name, rep_size, type, structure, num_genes, accession)"
        "VALUES ('{genome_id}', '{name}',' {rep_size}', '{replicon_type}', '{structure}','0','{accession}');"
        .format(genome_id=genome_id, name=name, rep_size=rep_size, replicon_type=replicon_type, structure=structure, accession=accession))
    cur.execute(sql_statement)
    #print("finish insert replicon", name)
    cur.close()



def update_replicon_gene_count(conn, replicon_id, count):
    cur = conn.cursor()
    sql_statement = ("UPDATE replicons "
        "SET num_genes = {count} "
        "WHERE replicon_id = {replicon_id}".format(count=count, replicon_id=replicon_id))
    cur.execute(sql_statement)
    #print("finish update replicon gene count",count)
    cur.close()

def insert_genes_table(conn, accession, genome_id, replicon_id, strand, name, locus_tag, num_exons, size, product):
    cur = conn.cursor()

    sql_statement = ("INSERT INTO genes(accession,genome_id,replicon_id,strand,name,locus_tag,num_exons,size,product)"
        "VALUES ('{accession}', '{genome_id}', '{replicon_id}', '{strand}','{name}', '{locus_tag}', '{num_exons}', '{size}', \"{product}\");"
        .format(accession=accession, genome_id=genome_id, replicon_id=replicon_id, strand=strand, name=name, locus_tag=locus_tag, num_exons=num_exons, size=size, product=product))
    #print(sql_statement)
    cur.execute(sql_statement)
    #print("finish insert gene", name)
    cur.close()

def insert_exons_table(conn, gene_id, left_position, right_position, size):
    cur = conn.cursor()

    sql_statement = ("INSERT INTO exons(gene_id, left_position, right_position, size) "
        "VALUES ('{gene_id}', '{left_position}', '{right_position}', '{size}')"
        .format(gene_id=gene_id, left_position=left_position, right_position=right_position, size=size))
    cur.execute(sql_statement)
    cur.close()

def load_genomes_table(conn):
    cur = conn.cursor()
    '''
    mutex_creation = ("create table mutex(i int not null primary key);"
        "insert into mutex(i) values (1);")
    '''
    sql_statement = ("LOAD DATA LOCAL INFILE 'genomes.tab' INTO TABLE genomes"
        "(genome_short_name,genome_long_name,domain,size,release_date,tax_id);")
    #cur.execute(mutex_creation)
    cur.execute(sql_statement)
    cur.close()

def load_replicons_table(conn):
    cur = conn.cursor()
    sql_statement = ("LOAD DATA LOCAL INFILE 'replicons.tab' INTO TABLE replicons"
        "(genome_id,name,rep_size,type,structure,num_genes,accession);")
    cur.execute(sql_statement)
    cur.close()

def load_genes_table(conn):
    cur = conn.cursor()
    sql_statement = ("LOAD DATA LOCAL INFILE 'genes.tab' INTO TABLE genes"
        "(gene_id, accession, genome_id, replicon_id, strand, name, locus_tag, num_exons, size, product);")
    cur.execute(sql_statement)
    cur.close()


def load_exons_table(conn):
    cur = conn.cursor()
    sql_statement = ("LOAD DATA LOCAL INFILE 'exons.tab' INTO TABLE exons"
        "(gene_id, left_position, right_position, size);")
    cur.execute(sql_statement)
    cur.close()

def load_synonyms_table(conn):
    cur = conn.cursor()
    sql_statement = ("LOAD DATA LOCAL INFILE 'gene_synonyms.tab' INTO TABLE gene_synonyms"
        "(gene_id, synonym);")
    cur.execute(sql_statement)
    cur.close()

def load_functions_table(conn):
    cur = conn.cursor()
    sql_statement = ("LOAD DATA LOCAL INFILE 'functions.tab' INTO TABLE functions"
        "(gene_id, function);")
    cur.execute(sql_statement)
    cur.close()

def import_genomes():
    os.system('mysqlimport -u root -p --local bimm185 --columns=genome_short_name,genome_long_name,domain,size,release_date,tax_id genomes.tab')

def import_replicons():
    os.system('mysqlimport -u root -p --local bimm185 --columns=genome_id,name,rep_size,type,structure,num_genes,accession replicons.tab')

def import_genes():
    os.system('mysqlimport -u root -p --local bimm185 --columns=gene_id,accession,genome_id,replicon_id,strand,name,locus_tag,num_exons,size,product genes.tab')

def import_exons():
    os.system('mysqlimport -u root -p --local bimm185 --columns=gene_id,left_position,right_position,size exons.tab')


def import_synonyms():
    os.system('mysqlimport -u root -p --local bimm185 --columns=gene_id,synonym gene_synonyms.tab')

def import_references():
    os.system('mysqlimport -u root -p --local bimm185 --columns=gene_id,external_db,external_id ex_references.tab')


def import_functions():
    os.system('mysqlimport -u root -p --local bimm185 --columns=gene_id,function functions.tab')

def main():
    os.system('mysql -u root -p bimm185 < create_tables.sql')
    myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, local_infile=True, autocommit=True)
    mx_genome_id = query_mx_genome_id(myConnection)

    #print("in main: ", mx_genome_id)
    mx_replicon_id = query_mx_replicon_id(myConnection)
    mx_gene_id = query_mx_replicon_id(myConnection)

    input_files = sys.argv[1:]
    #print(input_files)
    read_genbank(input_files,myConnection)
    load_replicons_table(myConnection)
    print('finish loading replicons')
    load_genes_table(myConnection)
    print('finish loading genes')
    load_exons_table(myConnection)
    print('finish loading exons')
    load_synonyms_table(myConnection)
    print('finish loading synonyms')
    load_functions_table(myConnection)
    print('finish loading functions')
    #load_genomes_table(myConnection)
    #load_replicons_table(myConnection)
    #os.system('mysql -u root -p bimm185 < create_tables.sql')
    '''
    import_genomes()
    import_replicons()
    import_genes()
    import_exons()
    import_synonyms()
    import_references()
    import_functions()
    '''
    myConnection.close()

if __name__ == '__main__':
    main()