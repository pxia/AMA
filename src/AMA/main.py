
import sys, util;

def ask():
    print "ask"
    articleFile = sys.argv[1]
    nquestions  = int(sys.argv[2])

    D = {"a":[1,2,3], "b":[2], "c":[2,1]}
    print [k for k in D.keys() if len(D.get(k))==min([len(n) for n in D.values()])][0]


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

# 	for kw in keywords:
# 		D[kw] = [i for i, w in enumerate(document) if w == kw]

# 	minAreaStart = 0	
# 	minAreaEnd = len(document)
# 	allOccurrences = [i for i, w in enumerate(document) if w in keywords]
# 	firstArea = 0
# 	areaMemberInd = []

# 	# find the initial area
# 	keywordToFind = keywords
# 	while (len(keywordToFind) > 0):
# 		if document[firstArea] in keywordToFind:
# 			areaMemberInd += [firstArea]
# 			keywordToFind.remove(document[area])
# 		firstArea += 1

# 	curSmallestArea = firstArea
# 	firstToDrop = document[areaMemberInd[0]]
# 	firstToGet = findPostNeighbor(areaMemberInd[-1], firstToDrop, D)
# 	frontDelta = areaMemberInd[1] - firstToDrop
# 	backDelta = firstToGet - areaMemberInd[-1]
# 	if (backDelta < frontDelta):
# 		curSmallestArea = curSmallestArea - frontDelta + backDelta

# 	areaMemberInd = areaMemberInd[1:]
# 	areaMemberInd += []



