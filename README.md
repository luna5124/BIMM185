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

## Week 2
## Exercise 1
* Copy the folder dirtree to your account (located in ../public/data/terminal/dirtree).
* Inside dirtree there are many directories, inside each directory there is another directory with the same name (e.g., 1.A.14_vs_1.A.26/ 1.A.14_vs_1.A.26/), and inside the second directory there is a file named report.tbl 
* To verify this information, inside dirtree try the command:  ls */*/*.tbl
* The results in report.tbl are sorted in descending order.
* For each directory in dirtree extract the top GSAT Z-score (row 3, column 4) from file report.tbl and generate an output file with to columns (base dir and Z-score) sorted in descending order by the Z-score:

```
2.A.123_vs_3.E.1		67
2.A.58_vs_9.A.14		19
1.A.76_vs_9.A.14		18
2.A.102_vs_2.A.112		18
…
```
## Exercise 2
From the NCBI Genome database, download the genome annotation in tabular format for E. coli K12 MG1655. Using shell commands to process the data.
*The genome annotation file header is:*

| Column # | Header |
| --- | --- |
| 1  | Replicon Name |
| 2 | Replicon Accession |
| 3 | Start |
| 4 | Stop |
| 5 | Strand |
| 6 | GeneID |
| 7 | Locus |
| 8 | Locus tag |
| 9 | Protein product |
| 10 | Length |
| 11 | COGS(s) |
| 12 | Protein name |

**Exercise problems and solutions:**
* What is the name (locus) and length of the largest protein?


    ```
    cut -f 7,10 table.txt | sort -k2nr | head -1
    ```
* What is the name and length of the smallest protein?


    ```
    cut -f 7,10 table.txt | sort -k2n | head -1
    ```
    
* How many proteins are in the forward strand?

    
    ```
    cut -f 5 table.txt | grep '+' | wc -l
    ```
* How many proteins are in the reverse strand?
    
    ```
    cut -f 5 table.txt | grep '-' | wc -l
    ```
* What is the largest protein in the forward strand?

    ```
    cut -f 5,7,10 table.txt | grep '+' | sort -k3nr | head -1
    ```
* What is the largest protein in the reverse strand?

    ```
    cut -f 5,7,10 table.txt | grep '-' | sort -k3nr | head -1
    ```
* What are the gene names (locus) of all ribosomal proteins in the genome?

    ```
    cut -f 7,12 table.txt | grep ribosomal
    ```


## Exercise 3
* From the NCBI Genome database, download the DNA sequence of the full E. coli K12 MG1655 genome and its annotation in tabular format. Write a script that: 
    * Reads the DNA sequence of the genome.
    * For each gene in the tab-separated annotations file, extract the DNA sequence and save it in a file in FASTA format.
    * If the protein is in the reverse strand you will have to complement the DNA sequence and reverse it, so it is displayed in the 5’ to 3’ direction in the output file.
    * Split each gene sequence in segments of 70 nucleotides before saving it.
    * This is the format that each sequence should use:

    ```
    >NP_414543.1|thrA|b0002
    ATGCGAGTGTTGAAGTTCGGCGGTACATCAGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCGATATTC
    TGGAAAGCAATGCCAGGCAGGGGCAGGTGGCCACCGTCCTCTCTGCCCCCGCCAAAATCACCAACCACCT
    GGTGGCGATGATTGAAAAAACCATTAGCGGCCAGGATGCTTTACCCAATATCAGCGATGCCGAACGTATT
    TTTGCCGAACTTTTGACGGGACTCGCCGCCGCCCAGCCGGGGTTCCCGCTGGCGCAATTGAAAACTTTCG
    TCGATCAGGAATTTGCCCAAATAAAACATGTC…TGA
    ```

## Mini Project
**Project description:**

In this project, we want to calculate the CUI(Codon Usage Index) for each protein in E.coli K12 MG1655 to testify our hypothesis on protein translatability that  If the genome has evolved to have most of its genes translated at adequate rates when it needs them, then the genomic frequencies of codons should be an adequate reference of translatability. We first generate a matrix, counting the occurrences of 64 codons for each gene as well as for all the genes in E.coli. Then we will use the matrix to calculate the frequency of each codon and then the CUI for each gene and all the genes.

![CUI equation](http://www.sciweavers.org/upload/Tex2Img_1492556891/render.png)

Finally, a histogram of the CUIs in E.coli is plotted.
