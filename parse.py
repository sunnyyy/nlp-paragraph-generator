from nltk.parse.bllip import BllipParser
from nltk.tokenize import word_tokenize
from nltk import pos_tag 
from nltk.data import find
from nltk.parse import stanford
#import bllipparser

#initializes parser using bllip parsing model described by nltk parsers api
#allows parsing of sentences with or without pos_tags 
def initialize_parser():
    model_dir = find('models/bllip_wsj_no_aux').path
    print('Loading BLLIP Parsing models...')

    bllip = BllipParser.from_unified_model_dir(model_dir)
    print('Done.')
    return bllip

#more pseudocode than anything, depends what parsed sentences look like
#if stanford parser then a tree format and have to learn how to iterate through trees.
def is_complete(parser,sentence):
    output = parser.parse(sentence)
    return output[0] == 'S'

def parse_sentences(parser, sentences):
    result = []
    incomplete_sentence = ''
    for s in sentences:
        if is_complete(parser,s):
            result.append(s)
        #dependent on how the tree works and how to look through it, more complicated, above could potentially work
        #if on a longer time frame.
        else:
            if incomplete_sentence == '':
                incomplete_sentence = s
            else:
                incomplete_parse = parser.parse(incomplete_sentence) 
                new_parse = parser.parse(s)


if __name__ == 'main':
    #parser = initialize_parser()
