(select b.qseqid, b.sseqid, b.bitscore,b.qcovs, b.scov from blast_1 b, 
	(select b1.qseqid, max(bitscore) as bitscore 
		from blast_1 b1 
		group by b1.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid 
	and b.bitscore = maxtable.bitscore) b1max;

(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_2 b, 
	(select b2.qseqid,max(bitscore) as bitscore 
		from blast_2 b2 
		group by b2.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid 
	and b.bitscore = maxtable.bitscore) b2max;


select b1max.qseqid, b1max.sseqid, b1max.bitscore, b1max.qcovs, b1max.scov, b2max.bitscore, b2max.qcovs, b2max.scov from 
(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_1 b, 
	(select b1.qseqid,max(bitscore) as bitscore from blast_1 b1 group by b1.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b1max, 
(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_2 b, 
	(select b2.qseqid,max(bitscore) as bitscore from blast_2 b2 group by b2.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b2max 
where b1max.qseqid = b2max.sseqid and b1max.sseqid = b2max.qseqid 
order by b1max.bitscore DESC;

mysql -root bimm185 -e'select b1max.qseqid, b1max.sseqid, b1max.bitscore, b1max.qcovs, b1max.scov, b2max.bitscore, b2max.qcovs, b2max.scov from 
(select b.qseqid, b.sseqid, b.bitscore,b.qcovs, b.scov from blast_1 b, (select b1.qseqid,max(bitscore) as bitscore from blast_1 b1 group by b1.qseqid) maxtable where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b1max;

(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_2 b, (select b2.qseqid,max(bitscore) as bitscore from blast_2 b2 group by b2.qseqid) maxtable where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b2max;

select b1max.qseqid, b1max.sseqid, b1max.bitscore, b1max.qcovs, b1max.scov, b2max.bitscore, b2max.qcovs, b2max.scov, 
from 
(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_1 b, 
	(select b1.qseqid,max(bitscore) as bitscore from blast_1 b1 group by b1.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b1max, 
(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_2 b, 
	(select b2.qseqid,max(bitscore) as bitscore from blast_2 b2 group by b2.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b2max 
where b1max.qseqid = b2max.sseqid and b1max.sseqid = b2max.qseqid 
order by b1max.bitscore DESC;' > BBHS.result


create view orthologs as select g1.gene_id as qid, g2.gene_id as sid, g2.replicon_id as rid from (select b1max.qseqid as qseqid, b1max.sseqid as sseqid from 
(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_1 b, 
	(select b1.qseqid,max(bitscore) as bitscore from blast_1 b1 group by b1.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b1max, 
(select b.qseqid, b.sseqid, b.bitscore, b.qcovs, b.scov from blast_2 b, 
	(select b2.qseqid,max(bitscore) as bitscore from blast_2 b2 group by b2.qseqid) maxtable 
	where b.qseqid = maxtable.qseqid and b.bitscore = maxtable.bitscore) b2max 
where b1max.qseqid = b2max.sseqid and b1max.sseqid = b2max.qseqid order by b1max.bitscore DESC) o1 inner join genes g1 on o1.qseqid = g1.accession inner join genes g2 on o1.sseqid = g2.accession;

