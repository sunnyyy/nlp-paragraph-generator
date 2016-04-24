from __future__ import division  # floating point division
from math import log
from nltk.tokenize import word_tokenize
import codecs #for unicode
import unicodecsv as csv
import sys

__author__ = "Sunnia Ye"

'''
***** TF part of TF-IDF *****
Input: a file + an option + a number k.
Returns: how many times each distinct word appears in a file.
Options:
- 0. DEFAULT: raw frequencies
- 1. log normalized
- 2. double normalization k
(k must be a float between 0 and 1; if not, default is set to 0.5)
'''
def term_freq(filename, option, k):
	tf = {}
	with codecs.open(filename, encoding='utf-8') as infile:
		for line in infile.readlines():
			tokens = word_tokenize(line)
			for term in tokens:
				if term in tf:
					tf[term] += 1
				else:
					tf[term] = 1
	if option == 1:
		# log normalization
		for term,freq in tf.iteritems():
			tf[term] = 1+log(freq)
	elif option == 2:
		# double normalization k
		maxfreq = max(tf.values())
		if k <= 0 or k >= 1 or isinstance(k, float)==False:
			k = 0.5
		for term,freq in tf.iteritems():
			tf[term] = k+(1-k)*(freq/maxfreq)
	'''
	with open(filename+'_tf.csv', 'w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
		for key,value in tf.iteritems():
			csvwriter.writerow([key,value])
	'''
	return tf

'''
**** HELPER METHOD for IDF ****
Input: a preprocessed csv file of docs per term 
Returns: a dictionary of terms --> docs per term
'''
def docs_per_word_parser(csvfile):
	wdc = {}
	with open(csvfile, 'r') as infile:
		csvreader = csv.reader(infile, delimiter=',', quotechar='"', encoding='utf-8')
		for row in csvreader:
			if row[0] in wdc:
				wdc[row[0]] += int(row[1])
			else:
				wdc[row[0]] = int(row[1])
	return wdc

'''
***** IDF part of TF-IDF *****
Input:
- csvfile = a preprocessed csv file of docs per term
- numdocs = number of total docs from which csvfile was derived
- option = type of idf weight
Returns: nothing
Output: csv file of terms --> idf values
Options:
- 0. DEFAULT: normal idf
- 1. smoothed idf
- 2. max idf
- 3. probabilistic idf
'''
def inv_doc_freq_v1(csvfile, option):
	# wdc is the number of files in which a word appears
	wdc = docs_per_word_parser(csvfile)
	idf = {}
	numdocs = 0
	with open('wdc/_num-'+csvfile[9:10]+'.txt', 'r') as ndfile:
		numdocs = int(ndfile.readline())
	
	if option == 1:
		# smoothed idf
		for key,value in wdc.iteritems():
			idf[key] = log(numdocs/(1+value))
	elif option == 2:
		# max idf
		maxterm = max(wdc.values())
		for key,value in wdc.iteritems():
			idf[key] = log(1+maxterm/value)
	elif option == 3:
		# probabilistic idf
		for key,value in wdc.iteritems():
			if numdocs-value > 0:
				idf[key] = log((numdocs-value)/value)
			else:
				idf[key] = 0
	else:
		# DEFAULT: plain idf
		for key,value in wdc.iteritems():
			idf[key] = log(numdocs/value)

	ops = ['','smoothed','max','probabilistic']
	with open('idf/idf_'+csvfile[9:10]+'-'+ops[option]+'.csv', 'w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
		for key,value in idf.items():
			csvwriter.writerow([key,value])

	#return idf



'''
***
'''
def tf_idf_v1(tf_file, idf_filelist):
	tf = term_freq(tf_file)
	idf = idf_preprocess(idf_file)
	tfidf = {}
	for key, value in tf:
		if key in idf:
			tfidf[key] = value * idf[key]
		else:
			tfidf[key] = 0 #if it never appears in ANY other docs, we assume a misspelling?
	return tfidf

def main(tf_file, idf_file):
	tf_idf_v1(tf_file, idf_file)

if __name__ == '__main__':
 	main(sys.argv[1], 'idf_0-smoothed.csv')




