#!/usr/bin/python
import sys, csv
from urlparse import urlparse

#process command line arguments
if len(sys.argv) < 3:
	print "ERROR: arg1: must specify the results file to format"
	print "       arg2: must specify the original corpus file"
	sys.exit(1)

#open files
results = open(sys.argv[1], "r")
finalRes = open("finalresults.csv", "wb")
corpus = open(sys.argv[2], 'rb')
reader = csv.reader(corpus, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
writer = csv.writer(finalRes, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

#get to the weka predictions section
lineval = ''
while '=== Predictions' not in lineval:
	lineval = results.readline()
results.readline()
results.readline()

#process each prediction line
for line in results.xreadlines():
	# read prediction line
	parts = line.split()
	if len(parts) < 3:
		break
	pred = parts[2].split(':')[1]
	
	# get corpus data and clean it up
	corpus_row = reader.next()
	tweet = corpus_row[4].replace('\n', ' ')
	
	# standardize URLs
	w = tweet.split()
	for i in range(len(w)):
		r = urlparse(w[i])
		if r[0] != '' and r[1] != '':
			w[i] = 'URL'
	tweet = ' '.join(w)
	corpus_row[4] = tweet
	
	# write output row
	writer.writerow( [corpus_row[2], corpus_row[0], pred, corpus_row[4]] )

#close files
results.close()
finalRes.close()
