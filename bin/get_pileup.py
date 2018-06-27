import os
import os.path
import argparse
from datetime import date
from collections import defaultdict
import subprocess
wd = os.path.dirname(os.path.realpath(__file__))
sra = wd + "/sra-pileup.2.9.1"
parser = argparse.ArgumentParser(description = "Fetch pileup files from SRA for given accessions")
#parser.add_argument('--user', type=argparse.FileType('r'), default=None)
parser.add_argument('-r', default=None)
parser.add_argument('-f', default=None)
parser.add_argument('-a', default= "./SraRunInfo.csv")
parser.add_argument('--temp',default= "./temp_pileup_" + str(date.today()))
parser.add_argument('--out', default= "autogenerated_allele_calling_" + str(date.today()) + ".csv")
#a = parser.parse_args(['--user', 'user_info.config'])
a = parser.parse_args()
if os.path.isfile(a.out):
	print("Error! output file {} already exists! Use another output file name!".format(a.out))
	exit(1)
if not os.path.isfile(a.a):
	print("Error! SRA run accessions file {} not exist or can't be accessed!".format(a.a))
	exit(1)
if os.path.exists(a.temp):
	print("Warning! temp directory {} already exists! It will not be cleared automatically to avoid"\
" deleting user files".format(a.temp))
	delete_temp = False
else:
	print("{} doesn't exist. Creating it now...".format(a.temp))
	subprocess.call(["mkdir", a.temp])
	delete_temp = True
if a.f:
#If a list of loci is provided
	call = wd + "/SRA_Get_pileup_list"
	subprocess.call([call, a.a, a.f, a.temp, sra])
elif a.r:
#If a list is not provided but a region is provided
	call = wd + "/SRA_Get_pileup"
	subprocess.call([call, a.a, a.r, a.temp, sra])
else:
#Neither a list or a region is provided, report error and exit
	print("Error! Either a region or a list of regions must be provided! Want whole genomoe data? Simply download their fastq files using fastq-dump from sra tools")
	exit(1)
#Creat a 2D dictionary to store alleles in each sample across loci
dict = defaultdict(dict)