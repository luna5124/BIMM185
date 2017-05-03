DROP TABLE IF EXISTS functions;
DROP TABLE IF EXISTS ex_references;
DROP TABLE IF EXISTS gene_synonyms;
DROP TABLE IF EXISTS synonyms;
DROP TABLE IF EXISTS exons;
DROP TABLE IF EXISTS genes;
DROP TABLE IF EXISTS replicons;
DROP TABLE IF EXISTS genomes;


CREATE TABLE genomes (
  	genome_id  	INT     (10) UNSIGNED NOT NULL AUTO_INCREMENT,
  	tax_id     	INT     (10) UNSIGNED NOT NULL,
  	domain     	ENUM('bacteria','archaea','eukarya') NOT NULL,
  	genome_short_name VARCHAR (100) NOT NULL,
  	genome_long_name VARCHAR (100) NOT NULL,
  	size 			INT 	(10) UNSIGNED NOT NULL,
 	release_date VARCHAR (100) NOT NULL,
  	PRIMARY KEY (genome_id),
  	KEY (tax_id)
)ENGINE=InnoDB;


CREATE TABLE replicons(
	replicon_id INT 	(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	genome_id 	INT 	(10) UNSIGNED NOT NULL,
	name 		VARCHAR (100) NOT NULL,
	num_genes 	INT 	(10) UNSIGNED NOT NULL,
	rep_size 	INT 	(10) UNSIGNED NOT NULL,
	accession 	VARCHAR (100)  NOT NULL,
	type ENUM('chromosome','plasmid','unknown') NOT NULL,
	structure ENUM('linear', 'circular') NOT NULL,
	PRIMARY KEY (replicon_id),
	FOREIGN KEY (genome_id) REFERENCES genomes(genome_id)
)ENGINE=InnoDB;


CREATE TABLE genes(
	gene_id 	INT 	(10) UNSIGNED NOT NULL,
	accession VARCHAR (100) NOT NULL,
	genome_id 	INT 	(10) UNSIGNED NOT NULL,
	replicon_id INT 	(10) UNSIGNED NOT NULL,
	locus_tag   VARCHAR (100) NOT NULL,
	name        VARCHAR (100) NOT NULL,
	strand 		ENUM('+','-')		  NOT NULL,
	num_exons 	INT 	(10) UNSIGNED NOT NULL,
	size 		INT 	(10) UNSIGNED NOT NULL,
	product     TEXT (1000) NOT NULL,
	PRIMARY KEY (gene_id),
	FOREIGN KEY (genome_id) REFERENCES genomes(genome_id),
	FOREIGN KEY (replicon_id) REFERENCES replicons(replicon_id)
)ENGINE=InnoDB;


CREATE TABLE exons(
	#--exon_id INT 	(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	gene_id INT 	(10) UNSIGNED NOT NULL,
	left_position INT 	(10) UNSIGNED NOT NULL,
	right_position INT 	(10) UNSIGNED NOT NULL,
	size INT 	(10) UNSIGNED NOT NULL,
	#--PRIMARY KEY (exon_id),
	#index(gene_id),
	#index(left_position),
	#index(right_position),
	FOREIGN KEY (gene_id) REFERENCES genes(gene_id)
)ENGINE=InnoDB;

CREATE TABLE gene_synonyms(
	gene_id INT 	(10) UNSIGNED NOT NULL,
	#--synonym_id INT (10) UNSIGNED NOT NULL,
	synonym VARCHAR (100) NOT NULL,
	#synonym_id INT (10) UNSIGNED NOT NULL,

	#--PRIMARY KEY (gene_id, synonym_id),
	#index(gene_id, synonym_id),
	PRIMARY KEY (gene_id, synonym)
	#FOREIGN KEY (gene_id) REFERENCES genes(gene_id),
	#FOREIGN KEY (synonym_id) REFERENCES synonyms(synonmy_id)
)ENGINE=InnoDB;

CREATE TABLE synonyms(
	synonym_id INT (10) UNSIGNED NOT NULL AUTO_INCREMENT,
	synonym VARCHAR (100) NOT NULL,
	PRIMARY KEY (synonym_id),
	KEY (synonym_id)
)ENGINE=InnoDB;


CREATE TABLE ex_references(
	gene_id INT 	(10) UNSIGNED NOT NULL,
	external_db	VARCHAR (100) NOT NULL,
	external_id VARCHAR 	(100) NOT NULL,
	index(gene_id, external_id),
	#--PRIMARY KEY (gene_id, external_db, external_id),
	FOREIGN KEY (gene_id) REFERENCES genes(gene_id)
)ENGINE=InnoDB;


CREATE TABLE functions(
	gene_id INT 	(10) UNSIGNED NOT NULL,
	function VARCHAR (256) NOT NULL,
	PRIMARY KEY (gene_id, function),
	KEY (gene_id)
)ENGINE=InnoDB;