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
VP_TAGS = ['VP', 'S', 'PP']
SYN_TAGS = ['ADJP', 'ADVP', 'NP', 'PP', 'S', 'SBAR', 'SBARQ', 'SINV', 'SQ', 'VP', 'WHNP', 'WHPP']
OBJ_TAGS = ['NP', 'ADJP', 'ADVP', 'PP']
NOUN_TAGS = ['NN', 'NNP', 'NNS', 'NNPS']
ADJ_TAGS = ['JJ', 'JJR', 'JJS']
ADV_TAGS = ['RB', 'RBR', 'RBS', 'RP']

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

def getObjects(objects):
    label = objects.label()
    if (label == 'NP'):
        return (0, processObjects(objects))
    elif (label == 'ADJP'):
        return (1, processObjects(objects))
    elif (label == 'ADVP'):
        return (2, processObjects(objects))
    elif (label == 'SBAR'):
        return (2, processObjects(objects))
    else:
        return (2, [])

def processObjects(objects):
    label = objects.label()
    if (label == 'NP'):
        return processNP(objects)
    elif (label == 'ADJP'):
        return processADJP(objects)
    elif (label == 'ADVP'):
        return processADVP(objects)
    elif (label == 'SBAR'):
        return processSBAR(objects)
    else:
        return []

def processNP(NP):
    if (type(NP) != nltk.tree.Tree): return []
    if (NP.label() in NOUN_TAGS):
        return [NP[0]]
    else:
        nouns = []
        for sub in NP:
            nouns += processNP(sub)
        return nouns

def processADJP(ADJP):
    if (type(ADJP) != nltk.tree.Tree): return [ADJP]
    if (ADJP.label() in ADJ_TAGS):
        return [ADJP[0]]
    else:
        adjs = []
        for sub in ADJP:
            adjs += processADJP(sub)
        return adjs


def processADVP(ADVP):
    if (type(ADVP) != nltk.tree.Tree): return [ADVP]
    if (ADVP.label() in ADV_TAGS):
        return [ADVP[0]]
    else:
        advs = []
        for sub in ADVP:
            advs += processADVP(sub)
        return advs

def processSBAR(SBAR):
    return [" ".join(SBAR.leaves())]




def preprocess(sentences):
    print "Start Processing ... "

    D1, D2, D3 = {}, {}, {}
    D = (D1, D2, D3)
    for sent in sentences:
        if sent == "": continue
        result = loads(corenlp.parse(sent))['sentences'][0]
        #dependencies = result['dependencies']
        parsetree = result['parsetree']
        tree = nltk.Tree.fromstring(parsetree)

        tree = tree[0]
        if (type(tree) == nltk.tree.Tree) and (len(tree) >= 2):
            NP, VP = tree[0], tree[1]

            subjects = getSubject(NP)
            (verbs, objects) = getVerbs(VP)
            (index, objs) = getObjects(objects)

            mapping = D[index]
            for verb in verbs:
                if verb not in mapping:
                    mapping[verb] = {}
                for subj in subjects:
                    if subj not in mapping[verb]:
                        mapping[verb][subj] = []
                    mapping[verb][subj].extend(objs)


            #print subjects, verbs
            #print objs
            #print

    return (D1, D2, D3)


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
data = util.readFile("text/0.txt").decode('utf8')
sentences = tokenizer.tokenize(data)
(D1, D2, D3) = preprocess(sentences)
print D1
