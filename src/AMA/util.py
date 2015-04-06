import nltk
import sys

def readFile(filename, mode="rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

def writeFile(filename, contents, mode="wt"):
    # wt stands for "write text"
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True

def pos_tag(sentence):
    return nltk.pos_tag(nltk.word_tokenize(sentence))

def removeTags(sentence):
    return zip(*sentence)[0]

def pos_tagContains(sentence, kw):
    for start in xrange(len(sentence)):
        for i in xrange(len(kw) + 1):
            if (i == len(kw)): return True
            if (sentence[start+i][0].lower() != kw[i].lower()): break
    return False

def extractKws(sentence):
    tree = nltk.ne_chunk(sentence, binary=True)
    return [removeTags(subtree.leaves())
        for subtree in tree.subtrees(lambda t: t.label() == "NE")] + \
        [tuple([word]) for (word, label) in sentence if label.startswith("NN")]

if __name__ == '__main__':
    pt = pos_tag("Welcome to Carnegie Mellon University.")
    print extractKws(pt)
