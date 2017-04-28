from Bio import SeqIO
import gzip
import sys
import os

'''
genome.tab format:
accession
genome_short_name
genome_long_name
domain
size
release_date
tax_id
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



def read_genbank(input_files):
    #read the gzipped input
    genome_file = open('genomes.tab','w')
    replicon_file = open('replicons.tab','w')
    gene_file = open('genes.tab','w')
    exon_file = open('exons.tab','w')
    synonym_files = open('synonyms.tab','w')
    j = 0
    for i in range(len(input_files)):
        cds_count = 0
        #gene_count = 0

        file = gzip.open(input_files[i],'rt')

        #print header
        #print('#accession','coordinates','strand','gene_name','locus_tag','synonyms','protein_name','Tax_ID','EC-numbers','external_references',sep='\t')
        #iterate through all the records in the input
        parses = SeqIO.parse(file,'genbank')

        for seq_record in SeqIO.parse(file,'genbank'):
            j += 1
            #seq_record = parses[j]
            #print('#',seq_record.id)
            #genome_file.write(seq_record.annotations['topology']+'\t')
            
            #write genome.tab

            #write replicon.tab
            replicon_file.write(str(i+1)+'\t')
            replicon_file.write(seq_record.description+'\t')
            replicon_file.write(str(len(seq_record.seq))+'\t')

            
            if 'chromosome' in seq_record.description:
                replicon_file.write('chromosome\t')
            elif 'plasmid' in seq_record.description:
                replicon_file.write('plasmid\t')
            else:
                replicon_file.write('unknown\t')

            replicon_file.write(seq_record.annotations['topology']+'\t')


            for f in seq_record.features:
               #check if it is CDS
                if f.type == "CDS":
                  #check if it has protein_id

                    if 'protein_id' in f.qualifiers:
                        accession = ','.join(f.qualifiers['protein_id'])

                        #gene_file.write(','.join(f.qualifiers['protein_id'])+'\t')
                    elif 'pseudo' in f.qualifiers:
                        #print(','.join(f.qualifiers['gene']),end='\t')
                        accession = 'pseudo'
                        
                        #gene_file.write('pseudo\t')
                    else:
                        #print(','.join(f.qualifiers['gene']),end='\t')
                        accession = 'i don\'t know\t'
                        #gene_file.write('i don\'t know\t')
                    gene_file.write(accession + '\t')
                    gene_file.write(str(i+1)+'\t')
                    gene_file.write(str(j)+'\t')
                   #get location
                    #print(f.location.start,f.location.end,sep='-',end='\t')
                    
                    #forward strand = 1, reverse strand = -1
                   
                    if f.location.strand == 1:
                        gene_file.write('+\t')
                    elif f.location.strand == -1:
                        gene_file.write('-\t')
                    
                    #print gene name
                    if 'gene' in f.qualifiers:
                        gene_file.write(','.join(f.qualifiers['gene'])+'\t')
                    else:
                        gene_file.write('-\t')

                   #print locus tag
                    if 'locus_tag' in f.qualifiers:
                        gene_file.write(','.join(f.qualifiers['locus_tag'])+'\t')
                    else:
                        gene_file.write('-\t')

                     #print synonym
                    '''
                    if 'gene_synonym' in f.qualifiers:
                        gene_file.write(','.join(f.qualifiers['gene_synonym']).replace('; ',','))
                        #GSs = f.qualifiers['gene_synonym']
                        #print(','.join(GSs),end='\t')
                    else:
                        gene_file.write('-')
                    '''
                    gene_file.write(str(len(f.location.parts)) + '\t')
                    gene_file.write(str(len(f.location)) + '\t')
                    
                    for e in f.location.parts:
                        exon_file.write(str(cds_count+1)+'\t')
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
                    if 'product' in f.qualifiers:
                        gene_file.write(','.join(f.qualifiers['product'])+'\t')
                    else:
                        gene_file.write('-\t')

                    #gene_file.write(taxid+'\t')
                    

                    #print EC_number
                    '''
                    if 'EC_number' in f.qualifiers:
                        gene_file.write(','.join(f.qualifiers['EC_number']))
                    else:
                        gene_file.write('-')
                      
                    #print external references
                    if 'db_xref' in f.qualifiers:
                        gene_file.write(','.join(f.qualifiers['db_xref']))
                    else:
                        gene_file.write('-')
                    ''' 
        
                    #change new line
                    gene_file.write('\n')
                    cds_count += 1
                #obtain taxid from source line
                elif f.type == 'source':
                    taxid = ','.join(f.qualifiers['db_xref']).replace('taxon:','')

            replicon_file.write(str(cds_count)+'\n')
        genome_file.write(seq_record.name+'\t')
        long_name = seq_record.annotations['source']
        short_name = '_'.join(long_name.split()[:2])
        genome_file.write(short_name + '\t')
        genome_file.write(long_name+'\t')
        genome_file.write('bacteria\t')
        genome_file.write(str(len(seq_record.seq))+'\t')
        genome_file.write(seq_record.annotations['date']+'\t')
        genome_file.write(taxid+'\n')
        file.close()
    genome_file.close()
    replicon_file.close()

def import_genomes():
    os.system('mysqlimport -u root -p --local bimm185 --columns=accession,genome_short_name,genome_long_name,domain,size,release_date,tax_id genomes.tab')

def import_replicons():
    os.system('mysqlimport -u root -p --local bimm185 --columns=genome_id,name,rep_size,type,structure,num_genes replicons.tab')

def import_genes():
    os.system('mysqlimport -u root -p --local bimm185 --columns=accession,genome_id,replicon_id,strand,name,locus_tag,num_exons,size,product genes.tab')

def import_exons():
    os.system('mysqlimport -u root -p --local bimm185 --columns=gene_id,left_position,right_position,size exons.tab')

def main():

    input_files = sys.argv[1:]
    #print(input_files)
    read_genbank(input_files)
    os.system('mysql -u root -p bimm185 < create_tables.sql')
    import_genomes()
    import_replicons()
    import_genes()
    import_exons()


if __name__ == '__main__':
    main()