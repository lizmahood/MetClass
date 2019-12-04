#!/usr/bin/env python3

import sys, glob, re

if (len(sys.argv) != 3):
	print('ARGS: 1) Full path to parsed main output file'\
		  '2) Full path to the original _augmented2.tab file')
	sys.exit()

fil = sys.argv[1]
fo = open(sys.argv[2], 'r')
lines = fo.readlines()
##get IDs of all lines in the file
ids = []
lids = []
with open(fil, 'r') as thisfil:
	lin = thisfil.readline().strip()
	##repeating to skip header
	lin = thisfil.readline().strip()
	
	while lin:
		ids.append(lin.split('\t')[0])
		lids.append('L' + lin.split('\t')[0])
		lin = thisfil.readline().strip()
	
outfil = open(fil + '_augmented2.tab', 'w')
outfil.write('#ID\tNewFormula\tMIM\tNumofC\tH\tO\tN\tP\tS\tHtoC\tHtoO\tCtoO\t'\
			 'CtoN\tCtoS\tCtoP\tafterdecmass\tAMD\tRMD\n')

for i in lids:
	line = [x for x in lines if x.startswith(i)]
	outfil.write(line[0])
	
outfil.close()

print('Done!')