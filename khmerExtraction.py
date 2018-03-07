import sys
from subprocess import call


# k
# chromosome files
# refgene file

k = sys.argv[1]
path = sys.argv[2] # path to the refGene and preprocessed chromosome files
inputFile = sys.argv[3] # file with list of desired genes


geneFile = open(inputFile, 'r')
refGeneFile = open(path + "refGene.txt", 'r')


geneNames = geneFile.readlines()
refGene = refGeneFile.readlines()
geneInfo = dict()
numGenes = len(geneNames)
for i in range(numGenes):
	geneNames[i] = geneNames[i].rstrip()
	for line in refGene:
		if geneNames[i].lower() == line.split('\t')[12].lower():
			if geneNames[i] in geneInfo:
			
				geneInfo[geneNames[i]].append(line)
			else:
				geneInfo[geneNames[i]] = []
				geneInfo[geneNames[i]].append(line)
print "extracted isoforms"
results = open("normalisedKmerCount.txt", 'w')

from itertools import product
kmers = list(product('ACGT', repeat = 3))
kmers = map(lambda x: x[0] + x[1] + x[2], kmers)
numKmers = 64 
results.write("kmer")
for i in range(numKmers):
	results.write("\t" + kmers[i])
results.write("\n")
import numpy as np
for gene in geneInfo:
	print gene
	results.write(gene)
	chrom = geneInfo[gene][0].split('\t')[2]
	numIsoforms = len(gene)
	chromFile = open(path + chrom + ".fa1", 'r')
	chromLine = chromFile.readline()
	scores = np.zeros(numKmers)
	for isoform in geneInfo[gene]:
		isoformScores = np.zeros(numKmers)
		info = isoform.split('\t')
		starts = info[9].rstrip(',').split(',')
		fins = info[10].rstrip(',').split(',')
		numExons = int(info[8])
		seq = "" 
		for k in range(numExons):
			seq = seq + chromLine[int(starts[k])-1:int(fins[k])]
		i = 0
		while i < len(seq) - 2:
			kmer = seq[i:i+3]
			for k in range(numKmers):
				if kmer in kmers[k]:
					isoformScores[k] += 1
			i += 1
		if len(seq) > 0 :
			isoformScores = map(lambda x: x /len(seq), isoformScores)
			scores = map(lambda x, y: x + y, scores, isoformScores)
	scores = map(lambda x: x / numIsoforms, scores)
	for score in scores:
		results.write("\t" + str(round(score, 10)))
	results.write("\n")
	

results.close()
