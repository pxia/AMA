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
VP_TAGS = ['VP', 'S']

def getSubject(NP):
    if type(NP) != nltk.tree.Tree:
        return []
    else:
        last = NP[-1]
        l = getSubject(last)
        l = l + [" ".join(NP.leaves())]
        return l

def getVerbs(VP):
    if (VP.label() not in VP_TAGS):
        return ([], VP)
    else:
        if (len(VP) == 1):
            return getVerbs(VP[0])

        VB = VP[0]
        VP = VP[1]
        (verbs, objects) = getVerbs(VP)
        if verbs:
            verb = verbs[0]
            verb = " ".join(VB.leaves()) + " " + verb
        else:
            verb = " ".join(VB.leaves())
        return ([verb] + verbs, objects)

def getObjects(NP):
    pass


def preprocess(sentences):
    print "Start Processing ... "

    dependency_table = {}
    for sent in sentences:
        if sent == "": continue
        result = loads(corenlp.parse(sent))['sentences'][0]
        dependencies = result['dependencies']
        parsetree = result['parsetree']
        tree = nltk.Tree.fromstring(parsetree)
        #for dependency in dependencies:
            #relation = dependency[0]
            #if relation not in dependency_table:
            #    dependency_table[relation] = [(dependency[1], dependency[2])]
            #else:
            #    dependency_table[relation].append((dependency[1], dependency[2]))
        #print dependencies

        tree = tree[0]
        if len(tree == 2):
            NP, VP = tree[0], tree[1]

            subjects = getSubject(NP)
            (verbs, objects) = getVerbs(VP)

            print subjects, verbs
            print

    return dependency_table


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
data = util.readFile("text/1.txt").decode('utf8')
sentences = tokenizer.tokenize(data)
table = preprocess(sentences)
