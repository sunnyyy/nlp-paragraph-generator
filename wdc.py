from __future__ import division  # floating point division
from math import log
from nltk.tokenize import word_tokenize
import codecs #for unicode
import re
import unicodecsv as csv

__author__ = "Sunnia Ye"


'''
***
'''
def wdc_all_wiki():
	filelist = []
	a = ['A','B','C','D','E','F']
	b = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	for ia in a:
		for ib in b:
			for i in xrange(0, 10):
				filelist.append("wiki/"+ia+ib+"/wiki_0"+str(i))
			for i in xrange(10, 100):
				filelist.append("wiki/"+ia+ib+"/wiki_"+str(i))
	for f in filelist:
		num_docs, word_doc_count = split_wiki_articles(f)
		print "wiki file ",f
		with open('wdc/'+f[5:7]+'_'+f[8:]+'.csv', 'a') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
			for key,value in word_doc_count.iteritems():
				if int(value) > 1:
					csvwriter.writerow([key,value])
		with open('wdc/_num.csv', 'a') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csvwriter.writerow([f,num_docs])

def split_wiki_articles(filename):
	word_doc_count = {}
	num_docs = 0
	with codecs.open(filename, encoding='utf-8') as infile:
		doc = []
		for line in infile:
			if '</doc>' == line[0:6]:
				#searchobj = re.search(ur'[\w\s]*[t][itle="]+([\w\s()!%^&_\-.,;:]+)"', doc[0], flags=0)
				#if searchobj and len(doc) > 10:
				if len(doc) > 10:
					#print doc[0]
					num_docs += 1
					#title = searchobj.group(0)[8:-1]
					#print title
					wordset = set()
					for sentence in xrange(1, len(doc)):
						wordset = wordset.union(word_tokenize(doc[sentence]))
					for word in wordset:
						if word in word_doc_count:
							word_doc_count[word] += 1
						else:
							word_doc_count[word] = 1
					'''
					with open('split/'+title+'.txt', 'w') as outfile:
						for sentence in range(1, len(doc)):
							outfile.write(doc[sentence])
					'''
				doc = []
			else:
				doc.append(line)
	return num_docs, word_doc_count

def merge_csvs(outfilename):
	filelist = []
	#a = ['F']
	a = ['A','B','C','D','E','F']
	#b = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	'''
	for ia in a:
		for ib in b:
			for i in xrange(0, 10):
				filelist.append("wdc/"+ia+ib+"_wiki_0"+str(i)+'.csv')
			for i in xrange(10, 100):
				filelist.append("wdc/"+ia+ib+"_wiki_"+str(i)+'.csv')
	'''
	for ia in a:
		filelist.append("wdc/_wdc-"+ia+'.csv')

	d = {}
	for f in filelist:
		with open(f, 'r') as infile:
			csvreader = csv.reader(infile, delimiter=',', quotechar='"', encoding='utf-8')
			for row in csvreader:
				if row[0] in d:
					d[row[0]] += int(row[1])
				else:
					d[row[0]] = int(row[1])
			print f
	with open('wdc/_wdc-'+outfilename+'.csv', 'a') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
		for k,v in d.iteritems():
			#log(1868991/(1+v)
			csvwriter.writerow([k,v])

'''
specifically deals with '_num.csv' file
'''
def count_num_docs(group):
	print group
	d = {}
	with open('wdc/_num.csv', 'rU') as infile:
		csvreader = csv.reader(infile, delimiter=',', quotechar='"', encoding='utf-8')
		if group == 'all':
			for row in csvreader:
				print row[0]
				if row[0] in d:
					d[row[0]] += int(row[1])
				else:
					d[row[0]] = int(row[1])
		else:
			for row in csvreader:
				# specifically the 5th character in (e.g. "wiki/AA/wiki_00")
				if row[0][5:6] == group:
					print row[0]
					if row[0] in d:
						d[row[0]] += int(row[1])
					else:
						d[row[0]] = int(row[1])
	num_docs = sum(d.values())
	with open('wdc/_num_'+str(group)+'.txt', 'w') as outfile:
		outfile.write(str(num_docs))


def main():
	#wdc_all_wiki()
	#merge_csvs('all')
	count_num_docs('all')

if __name__ == '__main__':
 	main()