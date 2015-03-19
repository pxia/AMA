import re

def ask():
    print "ask"

def answer():
    print "answer"



# assume document is accessible within the class, 
# and is already parsed into a raw string
def locateKeywords(keywords):
	D = {}
	for kw in keywords:
		D[kw] = map(lambda m: m.start(), re.finditer(kw, document))

	# find the area that the keywords are densest in


	


