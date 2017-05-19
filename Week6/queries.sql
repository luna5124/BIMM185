--all directons
select genes.gene_id, genes.name, strand, left_position, right_position from genes inner join
	(select gene_id, min(left_position) as left_position, max(right_position) as right_position 
			from exons group by gene_id) position 
	on position.gene_id = genes.gene_id where genes.genome_id = 1 order by left_position;


--find unique genes in A. tumefaciens
select * from genes A Where A.locus_tag not in (select locus_tag from genes where genome_id = 1);

--find unique genes in E.coli
select * from genes A Where A.locus_tag not in (select locus_tag from genes where genome_id = 2);

--find shared genes between E.coli and A.tumefaciens
select * from genes A, genes B where A.accession = B.accession and A.genome_id != B.genome_id and A.accession != 'pseudo';


select * from (select * from genes where genome_id = 1) A inner join (select * from genes where genome_id = 2)B on A.locus_tag = B.locus_tag;

--What are the predominant functions of the genes shared?


--What are the functions of the genes not shared?

--What transport systems are shared and which are not?
--What metabolic pathways are share and which are not?
--What about transcriptional regulators?
--How many proteins are syntenic?

