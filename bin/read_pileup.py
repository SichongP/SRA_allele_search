#!/usr/bin/python

#Read pileup file list from ./pileup_files
#for each file
#read each line
#use a hash to store info
#hash[var_id][sample_id]={everything else}}

#calculate alternative allele frequencies for each variant each sample
#[var_id x sample_id]
# 	sample1	sample2	sample3
#variant1 freq	freq	freq
#variant2 freq	freq	freq
#variant3 freq	freq	freq

import os, os.path
import sys, traceback
import csv
import re
import pprint
def read_file(root, filename, varianthash, refhash):
	"""
	read data from a file and store into a hash
	"""
	genebank_ids = {}
	refseq_ids = {}
	for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"chr_equcab2")):
		chr, genebank, refseq = line.strip().split('\t',3)
		genebank_ids[genebank] = chr
		refseq_ids[refseq] = chr
	for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"chr_equcab3")):
		chr, genebank, refseq = line.strip().split('\t',3)
		genebank_ids[genebank] = chr
		refseq_ids[refseq] = chr
#	print(genebank_ids)
	for line in open(os.path.join(root, filename)):
#		print(line)
		chr, pos, ref, depth, match, a, c, g, t, ins, dele, something = line.strip().split('\t',11)
		a=re.sub('-A','',a)
		c=re.sub('-C','',c)
		g=re.sub('-G','',g)
		t=re.sub('-T','',t)
		if chr in genebank_ids:
			identifier=genebank_ids[chr]+','+pos
		elif chr in refseq_ids:
			identifier=refseq_ids[chr]+','+pos
		else:
			identifier=chr+','+pos
#		print(identifier)
		refhash[identifier] = ref
		if identifier not in varianthash:
			varianthash[identifier] = {}
		if identifier in varianthash:
			if filename in varianthash[identifier]:
				print("encountered duplicate files: ", identifier)
				sys.exit(0)
			if match:
				alt_ratio = 1-float(match)/float(depth)
			else:
				alt_ratio = 1
			if alt_ratio<0.3:
				varianthash[identifier][filename]="."
			elif alt_ratio>0.7:
				if float(a)>0:
					varianthash[identifier][filename]='AA'
				elif float(c)>0:
					varianthash[identifier][filename]='CC'
				elif float(g)>0:
					varianthash[identifier][filename]='GG'
				elif float(t)>0:
					varianthash[identifier][filename]='TT'
				elif not ins:
					ins=re.sub('[0-9]-','',ins)
					varianthash[identifier][filename]='I-'+ins+'|'+ins
				elif not dele:
					dele=re.sub('[0-9]-','',dele)
					varianthash[identifier][filename]='D-'+dele+'|'+dele
			else:
				if float(a)>0:
					varianthash[identifier][filename]=ref+'A'
				elif float(c)>0:
					varianthash[identifier][filename]=ref+'C'
				elif float(g)>0:
					varianthash[identifier][filename]=ref+'G'
				elif float(t)>0:
					varianthash[identifier][filename]=ref+'T'
				elif not ins:
					ins=re.sub('[0-9]-','',ins)
					varianthash[identifier][filename]=ref+'|I-'+ins
				elif not dele:
					dele=re.sub('[0-9]-','',dele)
					varianthash[identifier][filename]=ref+'|D-'+dele
#	print(varianthash)
	return varianthash
def main():
	varianthash={}
	refs={}
	start_dir = './temp_pileup_2018-06-27'
	print('Starting in:', os.path.abspath(start_dir))
	for root, dirs, files in os.walk(start_dir):
		for filename in files:
#			print(filename)
			read_file(root, filename, varianthash, refs)
	pprint.pprint(varianthash)
if __name__ == "__main__":
	main()
