
def ask():
    print "ask"

    D = {"a":[1,2,3], "b":[2], "c":[2,1]}
    print [k for k in D.keys() if len(D.get(k))==min([len(n) for n in D.values()])][0]


def answer():
    print "answer"

# assume D's values are all sorted
def findPostNeighbor(curIndex, neighborKw, D):
    # 'Find leftmost value greater than x'
    i = bisect_right(D[neighborKw], curIndex)
    if i != len(a):
        return D[neighborKw][i]
    raise ValueError

# assume document is accessible within the class, 
# and is already tokenzied into a string list
def locateKeywords(keywords):
	D = {}

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



