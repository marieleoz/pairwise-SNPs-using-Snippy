#!/usr/bin/env python3

import os
import shutil
import subprocess

def extracSnps(file):
    """Parses a snps.csv output file from Snippy to count the ctSNPs (= SNPs
    that are bounded by at least 50 exact base-pair matches on both sides)."""
    nbSnps, position = 0,0
    osef = file.readline()
    while 1:
        fiLigne = file.readline()
        if fiLigne == "":
            break
        else:
            colonnes = fiLigne.split(",")
            if colonnes[2] == "snp":
                if position == 0:
                    position = int(colonnes[1])
                    nbSnps += 1
                elif int(colonnes[1]) > position + 50 or int(colonnes[1]) < position:
                    nbSnps += 1
                    position = int(colonnes[1])
    return nbSnps

#Lists the Reference files and infers the header for the output table
lisFi, lisRefs, lisR1, lisR2 = os.listdir(), [], [], []
for file in lisFi:
    if ".fasta" in file:
        lisRefs.append(file)
lisRefs.sort()
header = ","
for file in lisRefs:
    header += "{},".format(file)
header = "{}\n".format(header[:-1])

#Creates the snpsMatrix.csv output file, opens it and writes the header
fiSnps = open('snpsMatrix.csv','a')
fiSnps.write(header)

#Lists the R1 and R2 Query files
for file in lisFi:
    if "R1.fastq" in file:
        lisR1.append(file)
    elif "R2.fastq" in file:
        lisR2.append(file)
lisR1.sort()
lisR2.sort()

#Each Query is analyzed using Snippy,
#and its name used as first column of the corresonding line in the output file
for reads1 in lisR1:
    souche1 = reads1.split("R1")[0]
    for reads2 in lisR2:
        souche2 = reads2.split("R2")[0]
        if souche1 == souche2:
            reads = souche1
            ligneSnps = "{},".format(reads)
            #The current query is analyzed against all the references
            #A temporary subdirectory is created for each analysis
            for ref in lisRefs:
                ana = "ref{}_reads{}".format(ref.split("_")[0],reads)
                print("parametres snippy:\noutdir = {}\nref = {}\nR1 = {}\nR2 = {}".format(ana,ref,reads1,reads2))
                cmd = "snippy --cpus 28 --outdir {} --ref {} --R1 {} --R2 {}"\
                .format(ana,ref,reads1,reads2)
                subprocess.call(cmd, shell=True)
                #The number of ctSNPs between ref and query is inferred
                #from Snippy's snps.csv output file
                with open("{}/snps.csv".format(ana),"r") as ficsv:
                    snps = extracSnps(ficsv)
                ligneSnps += "{},".format(str(snps))
                #All output files from Snippy but snps.csv and snps.vcf are removed
                os.rename("{}/snps.csv".format(ana),"{}_snps.csv".format(ana))
                os.rename("{}/snps.vcf".format(ana),"{}_snps.vcf".format(ana))
                shutil.rmtree(ana)
    #Once the Query has been compared to all the References,
    #the respective ctSNP counts are added in the output file
    ligneSnps = "{}\n".format(ligneSnps[:-1])
    fiSnps.write(ligneSnps)
fiSnps.close()
