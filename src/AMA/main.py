from Article import Article
from util import *
import sys;
from bs4 import BeautifulSoup


def ask():
    # print "ask"
    articleFile = sys.argv[1]
    nquestions  = int(sys.argv[2])
    article     = getContent(readFile(articleFile))
    article     = "\n".join(map(normalize, article))
    A           = Article(article)
    # print A.D
    for q in A.ask(nquestions):
        print q

def answer():
    # print "answer"
    articleFile  = sys.argv[1]
    questionFile = sys.argv[2]
    article      = getContent(readFile(articleFile))
    article     = "\n".join(map(normalize, article))

    questions    = readFile(questionFile).splitlines()
    A            = Article(article)
    for question in questions:
        if len(question) != 0:
            print question
            print A.answer(question)
            print


# assume document is accessible within the class,
# and is already parsed into a raw string
def locateKeywords(keywords):
    D = {}
    for kw in keywords:
        D[kw] = map(lambda m: m.start(), re.finditer(kw, document))

    # find the area that the keywords are densest in

    for kw in keywords:
        D[kw] = [i for i, w in enumerate(document) if w == kw]

    minAreaStart = 0
    minAreaEnd = len(document)
    allOccurrences = [i for i, w in enumerate(document) if w in keywords]
    firstArea = 0
    areaMemberInd = []

    # find the initial area
    keywordToFind = keywords
    while (len(keywordToFind) > 0):
        if document[firstArea] in keywordToFind:
            areaMemberInd += [firstArea]
            keywordToFind.remove(document[area])
        firstArea += 1

    curSmallestArea = firstArea
    firstToDrop = document[areaMemberInd[0]]
    firstToGet = findPostNeighbor(areaMemberInd[-1], firstToDrop, D)
    frontDelta = areaMemberInd[1] - firstToDrop
    backDelta = firstToGet - areaMemberInd[-1]
    if (backDelta < frontDelta):
        curSmallestArea = curSmallestArea - frontDelta + backDelta

    areaMemberInd = areaMemberInd[1:]
    areaMemberInd += []
