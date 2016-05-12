# molynyk_smay_finalproject
*Final CS349 project*

**Write-up:**
https://docs.google.com/document/d/15XQ8kMllONRKe_YXe0vFFh-XI1hiEKpRkKRGZ2JBJ5s/edit

**Instructions for running:**
-- python 2.7
-- Stanford parser 
-- nltk

Run essaygenerator.py with the following keyword arguments: 
-- source document (string): one of the documents in the sourcedocs folder; provides the emissions/words that will appear in the output paragraph
-- style document (string): one of the documents in the sourcedocs folder; provides the part of speech transitions/”style” of the the output paragraph
-- keyword weight (integer): the multiplicative weight of the keywords selected by the TFIDF algorithm
-- number of keywords (integer): the number of keywords to be selected by the TFIDF algorithm
-- bigram weight (float between 0 and 1): the percentage of the emission probabilities that should come from bigram probabilities as opposed to emission probabilities in an HMM

The output paragraph will be written to a file and placed in the paragraphs folder.

Example:
Running:
>> python essaygenerator.py wellesley.txt sarah.txt 2 3 0.7
writes a paragraph with 3 keywords, weighted double, and uses 70% bigram and 30% emission probabilities.  It writes this paragraph to paragraphs/essay_wellesley_sarah-2.0_0.7.txt. 

----------

*Thurs, 4/7/2016, Project Update:*

1) Yes we met our milestone, our program output has original somewhat english text, it is legible if somewhat nonsensical, we didn't take in a thesis but we have themed source documents which helps narrow down the topic. However as we suspected we still have quite a ways to go before fooling anyone with our text.

2) So far we have an HMM which takes in a source corpus, where emissions are trained on, and a style corpus where transitions are trained on and this produces several sentences that sound vaguely English. We have also written a CFG and are in the process of writing the CKY algorithm to select the most grammatically correct of our sentences produced by the HMM and eliminate fragments. We have written a TF-IDF, and are in the process of testing it, and we will talk about application in the later question. 

3) Our results are a list of somewhat english sounding sentences, many of which are fragments, generated from an HMM with emissions traied on source documents (right now from wikipedia) and transitions trained on style documents supplied by the user whose 'paragraph' we wish to write. 

4) The results are not satisfacotry, there are many fragments produced so we plan to run the CKY algorithm over the POS tags of our produced sentences with a CFG we wrote to eliminate the fragments and select satisfactory sentences. Another problem is that the words in the sentence don't always follow a common theme making it very confusing to read and so we plan to incorporate aspects of a bigram model to combine with the HMM emission probabilities so that we select words not only based on the emission probability from the current state but also the probability based on the previous word. This might overfit but that's a problem for another day. Finally, we want to make sure that our paragraph accurately represents the information in the article so we plan to use TF-IDF to filter out the important words from source documents by artificially increasing their emission probabilities. 

5) See question 4, everything has changed. We are also playing around with the idea of training introductory or conclusion sentences off of body sentences produced. This will overfit but that's what you do in essays, or at least what I do in my essays. We may also just use a template for introductory and concluding sentences.

6) We will go and see you now. 

----------