import os
import sys
import subprocess

#Written by Misha Olynyk

'''
Creates a subprocess that runs the stanford nlp, putting the output into 
an output file which includes a parse tree.
WARNING, BEFORE RUNNING BE SURE THAT sampleProps.properties REFLECTS THE
INPUT FILE NAME.
'''
def run_parser():
    args = ['java','-Xmx1g','edu.stanford.nlp.pipeline.StanfordCoreNLP','-props','sampleProps.properties']
    p = subprocess.Popen(args)
    if os.path.isfile('input.txt.output'):
        p.terminate() #after results saved to file terminate the subprocess
'''
Analyze the output file, specifically the returned parse tree. And return
five non-fragment sentences by determining whether an S is present after ROOT
'''
def analyze_results(num_sents):
    f = open('input.txt')
    output = open('input.txt.output')
    input_lines = f.readlines()
    complete_sentences = []
    input_index = 0
    #print "I'm in this method"
    for line in output.readlines():
        if "<parse>" in line:
            if '(ROOT (S' in line:
                sentence = input_lines[input_index]
                complete_sentences.append(sentence[:len(sentence)-1])
            input_index += 1
            if len(complete_sentences) == num_sents:
                break
    return complete_sentences

def main(sents):
    run_parser()
    return analyze_results(sents)

if __name__ == '__main__':
    sents = int(sys.argv[1])
    run_parser()
    complete_sentences = analyze_results(sents)
    #print complete_sentences
