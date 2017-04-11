# BIMM185 - Bioinformatics Lab
## Week 1 - UNIX shell and basic text processing with Perl/Python. 
## Scripting Challenge 1
Read file TCDB.faa with protein sequences in fasta format. Parse the headers and extract the IDs, such that you reformat the file in two columns where the first column is the ID and the second column the sequence in a single string, that is:

```
>gnl|TC-DB|1002048004|2.A.4.5.2 CDF zinc transporter 2 [Russula atropurpurea]
MHFGLNDRPEQVASA
TTYNDPYNIAHGLKTD
SSRMDVNKWPVGGA
```

Will be printed as:

```
2.A.4.5.2-1002048004       MHFGLNDRPEQVASATTYNDPYNIAHGLKTDSSRMDVNKWPVGGA
```


## Scripting Challenge 2
Assume that file RS.txt.bz2 contains pairs of proteins (columns 1 and 2) that you predict are involved in physical interactions by the methods shown in column 3 with a given probability of interaction (column 4). 
Hypothetical scenario: A collaborator wants to test your predictions in the laboratory and will attempt to co-express, co-purify, co-crystallize, and solve the 3D structure of the binary hetero-complexes you predicted. However, he can only test your best predictions.
For the first 2000 different reference proteins in column 1, extract all their inferred binding partners (column 2), and report for each reference protein a) the candidate binding partner with the highest probability of interaction, and b) the total number of candidate binding partners for that reference protein.
* If we sort the resulting list of 2000 proteins by the probability column, we will be able to tell our collaborator which candidate interacting partners to take to the lab first. 
* In class we sorted by the number of interacting partners  to easily compare top results.
* If we plot the number of interacting partners vs the average (or top) probability of the interacting partners, we could try to answer the question of whether proteins that are involved in more interactions tend to be predicted with higher probability. Of course this is hypothetical as inference methods could overpredict or underpredict interactions, be biased, etc. But you get the idea…. 
