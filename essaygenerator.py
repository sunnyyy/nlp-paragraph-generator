from __future__ import division
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import codecs
import os
import argparse
import utils 
from tfidf import tf_idf_v1
import parse

"""
Given a source file (s), style file (t), and output file (o), generates strings of words to be used
in the body of a paragraph/essay summarizing s in the style of t.  Writes these strings to o. 

Emission probabilities are derived from a weighted average of HMM transition-emission probabilities 
(based on on s and t) and bigram probabilites (based only on s). 

The probability of certain key words from s, identified by the tfidf algorithm, are artificially increased.
"""
__author__ = 'S. May'

def tag_words_from_file(file):
	"""
	Given a file, returns a list of two-element tuples consisting of format (u'word', 'POS'), where word
	is a given word in the text and POS is its part of speech. Order of the words is maintained 
	Utilizes pos_tag from nltk.tokenize.
v	"""
	f = ''.join(codecs.open(file, encoding='utf-8').readlines())
	return pos_tag(word_tokenize(f))


def get_transitions(stylefile):
	"""
	Given a file, returns a nested dictionary of format {POS1: {POS1_1: Prob1_1, POS1_2: Prob1_2, ... } ... }.
	"""
	tags = [tup[1] for tup in tag_words_from_file(stylefile)]
	tags.insert(0, '.') # treat first word of file as if it follows period (e.g. is start of sentence)

	trans_counts = {}

	for i in xrange(1, len(tags)): 
		pos_1 = tags[i-1]
		pos_2 = tags[i]

		if pos_1 == '.': 
			if '#' not in trans_counts: 
				trans_counts['#'] = {}
			if pos_2 not in trans_counts['#']:
				trans_counts['#'].update({pos_2: 0})
			trans_counts['#'][pos_2] += 1

		if pos_1 not in trans_counts: 
			trans_counts[pos_1] = {}
		if pos_2 not in trans_counts[pos_1]: 
			trans_counts[pos_1].update({pos_2: 0})
		trans_counts[pos_1][pos_2] += 1

	trans_probs = {}

	for key, values in trans_counts.iteritems(): 
		trans_probs[key] = utils.normalize(values)

	return trans_probs

def get_emissions(sourcefile, keyword_weight, num_keywords): 
	"""
	Given source file, returns a nested dictionary of format {POS1: {EMIT1_1: Prob1_1, EMIT1_2: Prob1_2, ... } ... }.
	Probabilities of certain key words identified by the tfidf algorithm are artificially increased.
	"""
	tags = tag_words_from_file(sourcefile)

	tfidf_dict = tf_idf_v1(sourcefile, 'idf/idf_0-smoothed.csv')
	top_words = set(sorted(tfidf_dict.keys(), key= tfidf_dict.get, reverse=True)[:num_keywords]) 

	emit_counts = {}

	for tup in tags: 
		emit = tup[0]
		pos = tup[1]

		if pos not in emit_counts: 
			emit_counts[pos] = {}
		if emit not in emit_counts[pos]: 
			emit_counts[pos].update({emit: 0})

		# increase probabilities of key words
		if emit in top_words:
			emit_counts[pos][emit] += keyword_weight
		else:
			emit_counts[pos][emit] += 1

	emit_probs = {}

	for key, values in emit_counts.iteritems(): 
		emit_probs[key] = utils.normalize(values)

	return emit_probs

def get_relcounts(sourcefile):
	"""
	Given a file, returns a bigram relative counts dictionary.
	{tup[0]: tup[1]: value, tup1[1]: value1, ... 
	"""
	tokens = word_tokenize(''.join(codecs.open(sourcefile, encoding='utf-8').readlines()))

	tup_count = utils.tuple_count(tokens, 2)

	bigram = {}
	for tup, value in tup_count.items(): 
		if tup[0] not in bigram: 
			bigram[tup[0]] = {}
		if tup[1] not in bigram[tup[0]]: 
			bigram[tup[0]].update({tup[1]: value})

	for key, values in bigram.iteritems(): 
		bigram[key] = utils.normalize(values)
	return bigram

def generate(transitions, emissions, relcounts, bigram_weight):
    """
    Given transition and emission dictionaries, generate a list of symbols by randomly
    sampling the transition/emission dictionaries (HMM) until the emission is not '.'
    Emissions are based on both HMM transition emission and bigram probabilities, 
    in weights given by bigram_weight and (1-bigram_weight)
    """
    hmm_weight = 1-bigram_weight
    results = []
    # get / add start word
    state = utils.sample_from_dist(transitions.get('#'))
    emit = utils.sample_from_dist(emissions.get(state))
    if emit != None: 
    	results.append(emit.title())
    state = utils.sample_from_dist(transitions.get(state))

    # get / add remaining words 
    while state != '.':
    	emit_dict = emissions.get(state)
    	if emit in relcounts: 
    		rel_dict = relcounts.get(emit)
    		for key, value in emit_dict.items(): 
    			if key in rel_dict: 
    				emit_dict[key] = hmm_weight*value + bigram_weight*rel_dict[key]
    		emit_dict = utils.normalize(emit_dict)

    	emit = utils.sample_from_dist(emit_dict)
    	if emit != None: 
    		results.append(emit.lower())

    	state = utils.sample_from_dist(transitions.get(state))
    	while state not in emissions.keys():
    		state = utils.sample_from_dist(transitions.get(state))

    emit = utils.sample_from_dist(emissions.get(state))
    if emit != None: 
    	results.append(emit.lower())
    return results

def main():
	parser = argparse.ArgumentParser()

	# required arguments
	parser.add_argument('sourcefile', type=str, help='source of information for paragraph')
	parser.add_argument('stylefile', type=str, help='essay in style of author')
	parser.add_argument('keyword_weight', type=float, 
		help="multiplicative weight of key words. e.g. a weight of 2 doubles probabilities of keywords")
	parser.add_argument('num_keywords', type=int,
		help="number of keywords to grab")
	parser.add_argument('bigram_weight', type=float,
		help="weight of bigram probability to be used in generating emissions, e.g. 0 means only uses HMM, 1 means only uses Bigram")

	args = parser.parse_args()

	if args.bigram_weight > 1 or args.bigram_weight < 0:
		raise Exception("bigram_weight must be in range [0,1]")

	cd = os.getcwd()

	transitions = get_transitions(cd + "/sourcedocs/" + args.stylefile)
	print "transitions complete"

	emissions = get_emissions(cd + "/sourcedocs/" + args.sourcefile, args.keyword_weight, args.num_keywords)
	print "emissions complete"

	relcounts = get_relcounts(cd + "/sourcedocs/" + args.sourcefile)
	print "relcounts complete"

	
	# make output directory if none yet exists
	if not os.path.isdir("output"): 
		os.mkdir("output")

	outputfile = (args.sourcefile.split('.')[0] + "_" + args.stylefile.split('.')[0] 
		+ "-" + str(args.keyword_weight) + "_" + str(args.bigram_weight) + ".txt")

	o = codecs.open(cd + "/output/" + outputfile, 'a', 'utf8') 
	input_f = codecs.open('input.txt')
	o.write('\n\n****** NEW TRIAL ******\n')
	for _ in range(20):
		new_line = ' '.join(generate(transitions, emissions, relcounts, args.bigram_weight))
		o.write(new_line +'\n')
		input_f.write(new_line + '\n')

	print "written to:", "/output/"+outputfile

	parsed_sents = parse.main(5)
	print "\n", parsed_sents

	print "\nDONE"


if __name__ == '__main__':
	main()
