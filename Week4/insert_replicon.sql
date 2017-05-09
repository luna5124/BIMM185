INSERT INTO genomes (genome_short_name,genome_long_name, tax_id, domain) 
	      VALUES ('E_coli_K12_MG1655', 511145, 'bacteria'); 
INSERT INTO genomes (genome_short_name,genome_long_name, tax_id, domain) 
	      VALUES ('A_acidocaldarius', 521098, 'bacteria'); 
INSERT INTO genomes (genome_short_name,genome_long_name, tax_id, domain) 
	      VALUES ('S_cerevisiae', 559292, 'eukarya');




INSERT INTO replicons (replicon_id, genome_id, name, num_genes, rep_size) 
	      VALUES (1,1,'E_coli_K12_MG1655_chr', 4145, 4639675); 
INSERT INTO replicons (replicon_id, genome_id, name, num_genes, rep_size) 
	      VALUES (2,2,'A_acidocaldarius_chr', 2888, 3018755); 
INSERT INTO replicons (replicon_id, genome_id, name, num_genes, rep_size) 
	      VALUES (3,2,'A_acidocaldarius_pA', 98, 91726); 
INSERT INTO replicons (replicon_id, genome_id, name, num_genes, rep_size) 
	      VALUES (4,2,'A_acidocaldarius_pB', 92, 87298);
INSERT INTO replicons (replicon_id, genome_id, name, num_genes, rep_size) 
	      VALUES (5,3, 'S_cerevisiae_chr_I', 94,230218);
INSERT INTO replicons (replicon_id, genome_id, name, num_genes, rep_size) 
	      VALUES (6,3, 'S_cerevisiae_chr_II', 408,813184);