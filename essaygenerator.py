from __future__ import division
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import codecs
import os
import argparse
import numpy
import numpy.random
from utils import normalize, basic_count, length_count, tuple_count

"""
Uses HMM and bigrams to generate strings of words to be used in the body of a 
paragraph/essay. For the emission probabilities, uses a weighted average of HMM 
transition-emission probabilities and bigram probabilities. 

(not yet complete)The strings are parsed for grammatical correctness using the CYK 
algorithm and a grammar designed by the authors. 
"""
__author__ = 'S. May and Misha Olynyk'

def sample_from_dist(d):
    """given a dictionary representing a discrete probability distribution
    (keys are atomic outcomes, values are probabilities)
    sample a key according to the distribution.
    Example: if d is {'H': 0.7, 'T': 0.3}, 'H' should be returned about 0.7 of time.
    """
    # Do not modify this function
    roll = numpy.random.random()
    cumul = 0
    for k in d:
        cumul += d[k]
        if roll < cumul:
            return k

def tag_words_from_file(file):
	"""
	Given a file, returns a list of two-element tuples consisting of format (u'word', 'POS'), where word
	is a given word in the text and POS is its part of speech. Order of the words is maintained 
	Utilizes pos_tag from nltk.tokenize.
	"""
	f = ''.join(codecs.open(file, encoding='utf-8').readlines())
	return pos_tag(word_tokenize(f))


def get_transitions(sourcefile):
	"""
	Given a file, returns a nested dictionary of format {POS1: {POS1_1: Prob1_1, POS1_2: Prob1_2, ... } ... }.
	"""
	tags = [tup[1] for tup in tag_words_from_file(sourcefile)]
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
		trans_probs[key] = normalize(values)

	return trans_probs

def get_emissions(stylefile): 
	"""
	Given a file, returns a nested dictionary of format {POS1: {EMIT1_1: Prob1_1, EMIT1_2: Prob1_2, ... } ... }.
	Technically, only the parts of speech that are also in transitions dict will be used, since the paragraph/essay is in the style
	given by the transitions dictionary. 
	"""
	tags = tag_words_from_file(stylefile)

	emit_counts = {}

	for tup in tags: 
		emit = tup[0]
		pos = tup[1]

		if pos not in emit_counts: 
			emit_counts[pos] = {}
		if emit not in emit_counts[pos]: 
			emit_counts[pos].update({emit: 0})
		emit_counts[pos][emit] += 1

	emit_probs = {}

	for key, values in emit_counts.iteritems(): 
		emit_probs[key] = normalize(values)

	return emit_probs

def get_relcounts(sourcefile):
	"""
	Given a file, returns a nested n-gram relative counts dictionary, supporting
	unigrams and bigrams.  Add-1 smoothing is used.  
	"""
	tokens = word_tokenize(''.join(codecs.open(file, encoding='utf-8').readlines()))
	unigram = noramlize(basic_count(tokens))

	tup_count = tuple_count(tokens, 2)

	bigram = {}
	for tup, value in tup_count.items(): 
		if tup[0] not in bigram: 
			bigram[tup[0]] = {}
		if tup[1] not in bigram[tup[0]]: 
			bigram[tup[0]].update({tup[1]: value})


	#### normalize 

	return {1: unigram, 2: bigram}

def generate(transitions, emissions):
    """
    Given transition and emission dictionaries, generate a list of symbols by randomly
    sampling the transition/emission dictionaries (HMM) until the emission is not '.'
    """

    results = []
    state = sample_from_dist(transitions.get('#'))

    while state != '.': 
    	emit = sample_from_dist(emissions.get(state))
    	results.append(emit)
    	state = sample_from_dist(transitions.get(state))
    	while state not in emissions.keys():
    		state = sample_from_dist(transitions.get(state))

    emit = sample_from_dist(emissions.get(state))
    results.append(emit)
    
    return results

def main():
	parser = argparse.ArgumentParser()

	# required arguments
	parser.add_argument('sourcefile', type=str, help='source of information for paragraph')
	parser.add_argument('stylefile', type=str, help='essay in style of author')

	args = parser.parse_args()

	transitions = get_transitions(args.stylefile)
	print "transitions complete"

	emissions = get_emissions(args.sourcefile)
	print "emissions complete"

	with codecs.open('output.txt', 'a', 'utf8') as o: 
		o.write('****** NEW TRIAL ******\n')
		for _ in range(20):
			o.write(' '.join(generate(transitions, emissions))+'\n')

	print "DONE"


if __name__ == '__main__':
	main()