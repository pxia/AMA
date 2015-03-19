import sys, util;

def ask():
    print "ask"
    articleFile = sys.argv[1]
    nquestions  = int(sys.argv[2])

def answer():
    print "answer"
    articleFile  = sys.argv[1]
    questionFile = sys.argv[2]

    article      = readFile(article)
    questions    = util.readFile(questionFile).splitlines()



# assume document is accessible within the class,
# and is already parsed into a raw string
def locateKeywords(keywords):
    D = {}
    for kw in keywords:
        D[kw] = map(lambda m: m.start(), re.finditer(kw, document))

    # find the area that the keywords are densest in





