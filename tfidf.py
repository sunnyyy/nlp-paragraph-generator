from math import log

__author__ = "Sunnia Ye"

def term_freq(filename):
	wordcounts = {}
	with open(filename) as infile:
		for line in infile.readlines():
			line = line.strip()
			for word in line:
				if word in wordcounts:
					wordcounts[word] += 1
				else:
					wordcounts[word] = 1
	return wordcounts

def docs_per_word(filelist):
	word_doc_count = {}
	for filename in filelist:
		wordset = set(line.strip() for line in open(filename))
		for word in wordset:
			if word in word_doc_count:
				word_doc_count[word] += 1
			else:
				word_doc_count[word] = 1
	return word_doc_count

def inv_doc_freq(file_list):
	wdc = docs_per_word(filelist)
	idf = {}
	for key, value in word_dict:
		idf[key] = log(len(filelist)/(1+wdc[value]))
	return idf

def tf_idf(tf_file, idf_filelist):
	tf = term_freq(tf_file)
	idf = inv_doc_freq(idf_filelist)
	tfidf = {}
	for key, value in tf:
		if key in idf:
			tfidf[key] = value * idf[key]
		else:
			tfidf[key] = 0
	return tfidf