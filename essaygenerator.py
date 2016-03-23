from nltk import pos_tag
from nltk.tokenize import word_tokenize
import codecs
import os


# essaygenerator.py
__author__ = 'S. May and Misha Olynyk'


def normalize(countdict):
    """given a dictionary mapping items to counts,
    return a dictionary mapping items to their normalized (relative) counts
    Example: normalize({'a': 2, 'b': 1, 'c': 1}) -> {'a': 0.5, 'b': 0.25, 'c': 0.25}
    """
    total = sum(countdict.values())
    return {item: val/total for item, val in countdict.items()}

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
	Given a file, returns a nested dictionary of format {POS1: {POS1_1: Prob1_1, POS1_2: Prob1_2, ... }}.
	"""
	tags = [tup[1] for tup in tag_words_from_file(sourcefile)]
	tags.insert(0, '.') # treat first word of file as if it follows period (e.g. is start of sentence)

	trans_counts = {}

	for i in xrange(1, len(tags)): 
		if tags[i-1] not in trans_counts: 
			trans_counts[i-1] = {}
		if tags[i-1][i] not in trans_counts: 
			trans_counts[i-1][i] = 0
		trans_counts[i-1][i] += 1

	trans_probs = {}

	for key, values in trans_counts.iteritems(): 
		trans_probs[key] = normalize(values)

	return trans_probs


def main():
	parser = argparse.ArgumentParser()

	# required arguments
	parser.add_argument('sourcefile', type=str, help='source of information for paragraph')
	parser.add_argument('stylefile', type=str, help='essay in style of author')

	args = parser.parse_args()



if __name__ == '__main__':
	main()