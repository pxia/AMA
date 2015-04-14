import sys
import nltk
import re
import ner
import os

import util
from simplejson import loads
from lib.corenlp import StanfordCoreNLP
from nltk.stem.lancaster import LancasterStemmer



# print "Loading CoreNLP ... "
prevWd = os.getcwd()
os.chdir(os.path.split(os.path.realpath(__file__))[0])

corenlp_dir = "lib/stanford-corenlp-full-2014-08-27/"
corenlp = StanfordCoreNLP(corenlp_dir)  # wait a few minutes...

os.chdir(prevWd)


VP_TAGS = ['VP', 'S', 'VB'] #, 'PP']
SYN_TAGS = ['ADJP', 'ADVP', 'NP', 'PP', 'S', 'SBAR', 'SBARQ', 'SINV', 'SQ', 'VP', 'WHNP', 'WHPP']
OBJ_TAGS = ['NP', 'ADJP', 'ADVP', 'PP']
NOUN_TAGS = ['NN', 'NNP', 'NNS', 'NNPS']
ADJ_TAGS = ['JJ', 'JJR', 'JJS']
ADV_TAGS = ['RB', 'RBR', 'RBS', 'RP']
WH_TAGS = ['WHADJP', 'WHAVP', 'WHNP', 'WHPP']
WH_WORDS = ['what', 'when', 'why', 'who', 'whose', 'which', 'where']
BE_WORDS = ['is', 'are', 'were', 'was']
DO_WORDS = ['do', 'does', 'did']

def getSubject(NP):
    if type(NP) != nltk.tree.Tree:
        return [NP]
    else:
        last = NP[-1]
        l = getSubject(last)
        l = l + [" ".join(NP.leaves())]

        return l

def getVerbs(VP):
    if (type(VP) != nltk.tree.Tree):
        return ([], VP)

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
        return ([verb] + verbs
            , objects)

def getObjects(objects):
    # if objects == None:
    if (type(objects) != nltk.tree.Tree): return (-1, [])
    label = objects.label()
    if (label == 'NP'):
        return (0, processObjects(objects))
    elif (label == 'ADJP'):
        return (1, processObjects(objects))
    elif (label == 'ADVP'):
        return (2, processObjects(objects))
    elif (label == 'SBAR'):
        return (2, processObjects(objects))
    elif (label == 'PP'):
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
    elif (label == 'PP'):
        return processPP(objects)
    else:
        return []

def processNP(NP):
    if (type(NP) != nltk.tree.Tree): return []
    #if (NP.label() in NOUN_TAGS):
    #     return [NP[0]]
    #else:
    #    nouns = []
    #    for sub in NP:
    #        nouns += processNP(sub)
    #    return nouns
    return [" ".join(NP.leaves())]

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

def processPP(PP):
    return [" ".join(PP.leaves())]


def preprocess(sentences):
    # print "Start Processing ... "

    D1, D2, D3 = {}, {}, {}
    D = (D1, D2, D3)

    for sent in sentences:
        if len(sent) > 1000: continue
        if len(sent) == 0: continue
        if len(nltk.word_tokenize(sent)) <= 4: continue

        result = loads(corenlp.parse(sent))['sentences'][0]
        #dependencies = result['dependencies']
        parsetree = result['parsetree']
        tree = nltk.Tree.fromstring(parsetree)

        tree = tree[0]
        if (type(tree) == nltk.tree.Tree) and (len(tree) >= 2):
            NP, VP = tree[0], tree[1]

            subjects = list(set(getSubject(NP)))

            (verbs, objects) = getVerbs(VP)

            (index, objs) = getObjects(objects)

            if (index < 0): continue

            mapping = D[index]
            for verb in verbs:
                verb = verb.lower()
                if verb not in mapping:
                    mapping[verb] = {}
                for subj in subjects:
                    subj = subj.lower()
                    if subj not in mapping[verb]:
                        mapping[verb][subj] = []
                    mapping[verb][subj].extend(objs)


    D1 = {k: {p: list(set(q)) for p, q in v.items()} for k, v in D1.items()}
    D2 = {k: {p: list(set(q)) for p, q in v.items()} for k, v in D2.items()}
    D3 = {k: {p: list(set(q)) for p, q in v.items()} for k, v in D3.items()}
    return (D1, D2, D3)

def buildDatabase(D1, D2, D3):
    # Di's are dictionaries of dictionaries in the form:
    # D1 : relation_name -----> subject --> [(verb, object)] list
    # D2 : relation_name (verb) -----> subject --> [adv] list
    # D3 : relation_name (verb) -----> subject --> [adj] list

    # returns a dictionary of the form: subject ----> (list of) properties, where
    # a subject's property in the result dictionary contains the relation's name
    # and a list of verb-object/adv/adj relations

    D = {}
    for relation_name, inner_dict1 in D1.iteritems():
        for subject, verb_object_properties in inner_dict1.iteritems():
            subject = subject.lower()
            if not subject in D:
                D[subject] = []

            D[subject] += [(relation_name, verb_object_properties)]

    for verb_name, inner_dict2 in D2.iteritems():
        for subject, adv_properties in inner_dict2.iteritems():
            subject = subject.lower()
            if not subject in D:
                D[subject] = []
            D[subject] += [(verb_name, adv_properties)]

    for verb_name, inner_dict3 in D3.iteritems():
        for subject, adj_properties in inner_dict3.iteritems():
            subject = subject.lower()
            if not subject in D:
                D[subject] = []
            D[subject] += [(verb_name, adj_properties)]

    return D

#D1 = {"IN": {"Beth":[("live", "Pittsburgh"), ("born", "Nanjing")], "Joe":[("swim","pool"), ("study", "Gates")],
#            "Nathan":[("smoke","basement"), ("eat", "kitchen")]},
#     "ON": {"Beth":[("jump","table")], "Nathan":[("cry", "shoulder")]}}

#D2 = {"DANCE": {"Beth":["beautifully", "elegantly"], "Joe":["passionately","romantically"]},
#     "EAT": {"Nathan":["fast"], "Joe":["slowly"]}}

#D3 = {"BE": {"Beth":["medium-height", "lean","sporty"], "Nathan":["beardy", "lazy"], "Joe":["skinny"], "Jack":["dizzy", "blond"]},
#     "BECOME": {"Jack":["an actor", "the student president"], "Nathan":["musician", "fat"]}}

#print buildDatabase(D1, D2, D3)


"""
def restate_question_in_statement_form(question): # question is a string
    q = (filter(lambda ch: ch.isspace() or ch.isalpha(), question)).split(" ")
    firstWord = q[0].lower()
    secondWord = q[1].lower()

    # parse out subject and verb, insert firstWord after them but before everything else (aux clause)
    result = loads(corenlp.parse(question))['sentences'][0]
    parsetree = result['parsetree']
    tree = nltk.Tree.fromstring(parsetree)
    tree = tree[0]

    # what does he...? => he does what
    # when do we meet? => we meet when?
    # when is the show? => the show is when?
    # when is he making dinner? =? he is making dinner when?
    # whose book is this? => this is whose book?
    # which dog is his? => which dog is his

    res = []
    if (firstWord in WH_WORDS):
        if (secondWord in DO_WORDS):
            if (firstWord == 'what' or firstWord == 'which' or firstWord == 'who'):
                if (type(tree) == nltk.tree.Tree) and (len(tree) >= 2):
                    NP, VP = tree[0], tree[1]
                    verb = filter(lambda st: st.label() == 'VP', VP.subtrees())[0]
                    np = filter(lambda st: st.label() == 'NP', VP.subtrees())[0]

                    res = [" ".join(np.leaves())] + [" ".join(verb.leaves())] + [firstWord]

            elif (firstWord == 'where' or firstWord == 'when' or firstWord == 'why'):
                # insert firstWord after everything else, ommiting the DO_WORD
                res = q[2:] + [firstWord]

        elif (secondWord in BE_WORDS):
            if (type(tree) == nltk.tree.Tree) and (len(tree) >= 2):
                NP, VP = tree[0], tree[1]
                subjects = list(set(getSubject(NP)))
                (verbs, objects) = getVerbs(VP)

                VP = filter(lambda st: st.label() == 'VP', objects.subtrees())
                NP = filter(lambda st: st.label() == 'NP', objects.subtrees())[0]

                if VP: # what is he making for dinner
                    VP = VP[0]
                    VBG = filter(lambda st: st.label() == 'VBG', VP.subtrees())[0]
                    PP = filter(lambda st: st.label() == 'PP', VP.subtrees())[0]
                    res = [" ".join(NP.leaves())] + [secondWord] + [" ".join(VBG.leaves())] + [firstWord] + [" ".join(PP.leaves())]

                else: # what is a dog
                    res = [" ".join(NP.leaves())] + [secondWord, firstWord]

    elif (firstWord in BE_WORDS):
        if (type(tree) == nltk.tree.Tree) and (len(tree) >= 2):
            NP = tree[1]
            res = [" ".join(NP.leaves())] + [firstWord] + reduce(lambda x, y: x + y, map(lambda st: [" ".join(st.leaves())], tree[2:]))

    return " ".join(map(lambda x: str(x), res)) # get rid of weird utf8

def answer(question, D):
    st = LancasterStemmer()

    # for question in questions:
    # if question == "": continue

    reformed_question = restate_question_in_statement_form(question)
    print reformed_question

    result = loads(corenlp.parse(reformed_question))['sentences'][0]
    parsetree = result['parsetree']
    tree = nltk.Tree.fromstring(parsetree)

    tree = tree[0]
    if (type(tree) == nltk.tree.Tree) and (len(tree) >= 2):
        NP, VP = tree[0], tree[1]

        subjects = list(set(getSubject(NP)))

        (verbs, objects) = getVerbs(VP)

        (index, objs) = getObjects(objects)

        foundedAnswer = False

        if (D[subjects[0].lower()]):
            for (v, o) in D[subjects[0].lower()]:
                if st.stem(verbs[0].lower()) == st.stem(v.lower()):
                    firstWord = (question.split(" ")[0]).lower()
                    if firstWord in WH_WORDS:
                        return o[0]
                        foundedAnswer = True
                    elif firstWord in BE_WORDS:
                        return "Yes." if st.stem(objs[0].lower()) == st.stem(o[0].lower()) else "No."
                        foundedAnswer = True
        else: # who case
            for (sj, properties) in D.iteritems():
                for (v, p) in properties:
                    if str(verbs[0]) == str(v) and str(p) == str(objs):
                        return sj
                        foundedAnswer = True

        if not foundedAnswer:
            return "I don't know man."
"""



def keepLast(l):
    result = []
    s = []
    for word in l[::-1]:
        s = [word] + s
        result.append(" ".join(s))
    return result

def keepFirst(l):
    result = []
    s = []
    for word in l:
        s = s + [word]
        result.append(" ".join(s))
    return result

def findVP(tree):
    F = []
    NP = []

    if type(tree) != nltk.tree.Tree:
        return []
    if tree.label() in VP_TAGS:
        return tree
    else:
        F.append(tree)
        while F:
            T = F.pop(0)
            for sub in T:
                if type(sub) != nltk.tree.Tree:
                    continue
                if sub.label() in VP_TAGS:
                    return sub
                F.append(sub)
        return []

def trimTree(tree):
    while (len(tree) == 1):
        tree = tree[0]
    return tree




def eitherContains(phrase, l):
    if type(phrase) == str:
        phrase = phrase.lower()
        for tokens in l:
            tokens = tokens.lower()
            if phrase in tokens:
                return True
            if tokens in phrase:
                return True
        return False
    else:
        for p in phrase:
            p = p.lower()
            for tokens in l:
                tokens = tokens.lower()
                if p in tokens:
                    return True
                if tokens in p:
                    return True
        return False

def findMatchForSQ(subjs, verbs, objs, D):
    finded = False
    for subj in subjs:
        subj = subj.lower()
        if subj in D:
            tuples = D[subj]
            for (v, o) in tuples:
                if (eitherContains(v, verbs) and
                    eitherContains(o, objs)):
                    finded = True
    return finded



def answerSQ(tree):
    verbs = []
    subject = []
    objs = []

    if (tree[0].label() == "VP"):
        tree = tree[0]
        tree = trimTree(tree)

        qVerb = " ".join(tree[0].leaves())

        if (len(tree) == 2):
            S = tree[1]
            statement = " ".join(S.leaves())

            if (qVerb.lower() in DO_WORDS):
                S = trimTree(S)

                if (len(S) == 2):
                    NP = trimTree(S[0])
                    VP = trimTree(S[1])

                    if (VP.label() == "VP"):
                        subject = getSubject(NP)
                        (verbs, objects) = getVerbs(VP)
                        (index, objs) = getObjects(objects)
                    else:
                        if (type(NP) == nltk.tree.Tree):
                            words = NP.leaves()
                        else:
                            words = [NP]
                        words = NP.leaves()
                        subject = keepLast(words[:-1])
                        verbs = [words[-1]]
                        (index, objs) = getObjects(VP)
                else:
                    VP = findVP(S)
                    if (VP != []):
                        words = S.leaves()
                        VPwords = VP.leaves()
                        index = words.index(VPwords[0])
                        NPwords = words[:index]

                        subject = keepLast(NPwords)
                        (verbs, objects) = getVerbs(VP)
                        (index, objs) = getObjects(objects)

        else:
            S = tree[1:]
            parts = []
            for sub in S:
                parts.append(" ".join(sub.leaves()))
            statement = " ".join(parts)

            NP = trimTree(S[0])
            VP = trimTree(S[1])

            if (VP.label() == "VP"):
                subject = getSubject(NP)
                (verbs, objects) = getVerbs(VP)
                (index, objs) = getObjects(objects)
            else:
                if (type(NP) == nltk.tree.Tree):
                    words = NP.leaves()
                else:
                    words = [NP]
                subject = keepLast(words[:-1])
                verbs = [words[-1]]
                (index, objs) = getObjects(VP)
    else:
        verbs = [" ".join(tree[0].leaves())]
        subject = getSubject(tree[1])
        objects = tree[2]
        objs = []
        obj = []
        for sub in objects:
            if (type(sub) == nltk.tree.Tree):
                obj.append(" ".join(sub.leaves()))
            else:
                obj.append(sub)
            objs.append(" ".join(obj))
        if (verbs[0].lower() in BE_WORDS):
            statement = " ".join([subject[-1], verbs[0], objs[-1]])
        else:
            statement = " ".join([subject[-1], objs[-1]])

    return (subject, verbs, objs, statement)


def answerSBARQ(tree):
    pass

def answer(question, D):
    st = LancasterStemmer()

    # parse out subject and verb, insert firstWord after them but before everything else (aux clause)
    result = loads(corenlp.parse(question))['sentences'][0]
    parsetree = result['parsetree']
    tree = nltk.Tree.fromstring(parsetree)
    tree = tree[0]
    finded = True
    #print tree
    #print


    if (tree.label() == "SQ"):
        (subjs, verbs, objs, statement) = answerSQ(tree)
        finded = findMatchForSQ(subjs, verbs, objs, D)
        #print subjs
        #print verbs
        #print objs
        #print statement
        #print

        if finded:
            return "Yes."
        else:
            # NEED TO CHECK STATEMENT !!!
            return "No."
    elif (tree.label() == "SBARQ"):
        #print tree
        #print
        return "Fuck you!"
    elif (tree.label() == "S"):
        if (tree[0].label() == "VP"):
            (subjs, verbs, objs, statement) = answerSQ(tree)
            finded = findMatchForSQ(subjs, verbs, objs, D)
            if finded:
                return "Yes."
            else:
                # NEED TO CHECK STATEMENT !!!
                return "No."
        else:
            return "Fuck you!"
    else:
        return "Fuck you!"

sentences = []
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#for i in xrange(1):
#    path = "../../test/text/q" + str(i) + ".txt"
#    data = util.readFile(path).decode('utf8')
#    sentences += tokenizer.tokenize(data)

# (D1, D2, D3) = preprocess(sentences)
# D = buildDatabase(D1, D2, D3)
# print D
# qs = util.readFile("text/questions.txt").decode('utf8')
# questions = tokenizer.tokenize(qs)
# print answer(questions, D)


q0 = "Did William Herschel discover Uranus on 13 March 1781?"
q1 = "How many stars in the constellation are visible to observation on Earth without a telescope?"
q2 = "Which nebula resembles a person's head wearing a parka?"
q3 = "For how long does the Sun reside in the astrological sign of Gemini each year?"
q4 = "Approximately how many people speak English as their first language?"
q5 = "Do the Epsilon Geminids and Orionids peak at the same time?"
q6 = "Do the Geminids peak on November 13-14?"
q7 = "Do you like her?"
q8 = "Is Castor the second brightest star in Gemini?"
q9 = "Is she beautiful?"
q10 = "Who has been killed by the pollice?"
q11 = "Do violin and fiddle mean the same thing?"
q12 = "Do cellos have an endpin?"
Q = [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12]

#for q in sentences:
#    answer(q, {})
