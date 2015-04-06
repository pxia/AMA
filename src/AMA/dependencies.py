import sys
import nltk
import re
import ner

import util
from simplejson import loads
from lib.corenlp import StanfordCoreNLP



print "Loading CoreNLP ... "
corenlp_dir = "lib/stanford-corenlp-full-2014-08-27/"
corenlp = StanfordCoreNLP(corenlp_dir)  # wait a few minutes...

def preprocess(sentences):
    print "Start Processing ... "

    dependency_table = {}
    for sent in sentences:
        if sent == "": continue
        result = loads(corenlp.parse(sent))['sentences'][0]
        dependencies = result['dependencies']
        parsetree = result['parsetree']
        #for dependency in dependencies:
            #relation = dependency[0]
            #if relation not in dependency_table:
            #    dependency_table[relation] = [(dependency[1], dependency[2])]
            #else:
            #    dependency_table[relation].append((dependency[1], dependency[2]))
        print dependencies
        print parsetree
        print
    return dependency_table


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
data = util.readFile("text/0.txt").decode('utf8')
sentences = tokenizer.tokenize(data)
table = preprocess(sentences)
print table
