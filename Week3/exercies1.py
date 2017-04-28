from Bio import SeqIO
import gzip
import sys

#print string ends with tab
def print_function(s):
    print(s,end='\t')


def read_genbank(input_file):
    #read the gzipped input
    file = gzip.open(input_file,'rt')

    #print header
    print('accession','coordinates','strand','gene_name','locus_tag','synonyms','protein_name','Tax_ID','EC-numbers','external_references',sep='\t')

    #iterate through all the records in the input
    for seq_record in SeqIO.parse(file,'genbank'):

        for f in seq_record.features:
           #check if it is CDS
            if f.type == "CDS":
              #check if it has protein_id
                if 'protein_id' in f.qualifiers:
                    print_function(','.join(f.qualifiers['protein_id']))
                elif 'pseudo' in f.qualifiers:
                    #print(','.join(f.qualifiers['gene']),end='\t')
                    print_function('pseudo')
                else:
                    #print(','.join(f.qualifiers['gene']),end='\t')
                    print_function('i don\'t know')
               #get location
                print(f.location.start,f.location.end,sep='-',end='\t')
                
                #forward strand = 1, reverse strand = -1
                if f.location.strand == 1:
                    print_function('+')
                elif f.location.strand == -1:
                    print_function('-')
                
                #print gene name
                if 'gene' in f.qualifiers:
                    print_function(','.join(f.qualifiers['gene']))
                else:
                    print_function('-')

               #print locus tag
                if 'locus_tag' in f.qualifiers:
                    print_function(','.join(f.qualifiers['locus_tag']))
                else:
                    print_function('-')

               #print synonym
                if 'gene_synonym' in f.qualifiers:
                    print_function(','.join(f.qualifiers['gene_synonym']).replace('; ',','))
                    #GSs = f.qualifiers['gene_synonym']
                    #print(','.join(GSs),end='\t')
                else:
                    print_function('-')

               #print product name
                if 'product' in f.qualifiers:
                    print_function(','.join(f.qualifiers['product']))
                else:
                    print_function('-')


                print_function(taxid)

               #print EC_number
                if 'EC_number' in f.qualifiers:
                    print_function(','.join(f.qualifiers['EC_number']))
                else:
                    print_function('-')
                    
               #print external references
                if 'db_xref' in f.qualifiers:
                    print_function(','.join(f.qualifiers['db_xref']))
                else:
                    print_function('-')


                #change new line
                print()
            #obtain taxid from source line
            elif f.type == 'source':
                taxid = ','.join(f.qualifiers['db_xref']).replace('taxon:','')

    file.close()

def main():
    input_file = sys.argv[1]
    read_genbank(input_file)


if __name__ == '__main__':
    main()