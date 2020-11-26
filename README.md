# auto-ctSNPs-using-Snippy
Automation of SNP analysis using Snippy and parsing of the .csv output files for ctSNP count

This script has been used in the following article:
"Within-host microevolution ofPseudomonas aeruginosa urinaryisolates: a seven-patient longitudinalgenomic and phenotypic study"
Submitted to Frontiers in Microbiology
By Agnès Cottalorda et al.

It calls Snippy (https://github.com/tseemann/snippy/) for mapping and analysis of a series of raw reads onto a series of genome assemblies, and parses the snps.csv output files from each analysis to count the SNPs that are bounded by at least 50 exact base-pair matches on both sides (clone type SNPs - or ctSNPs - as defined by Marvig et al in https://pubmed.ncbi.nlm.nih.gov/25401299/).

Input files:
- References = genome assemblies in .fas format
- Queries = pairs of R1 and R2 raw read files in .fastq format
Output file: a snpsMatrix.csv table
