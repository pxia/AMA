
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

beVerb = set(["is", "are", "was", "were", "am"])
#verbTag = set(["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])
verbTag = {"VB":"Do", "VBD":"Did", "VBG":"Do", "VBN":"Did", "VBP":"Do", "VBZ":"Does"}

def yesNoQuestion(text, tags):
    lemmatizer = WordNetLemmatizer()
    verbIndex = None
    beQuestion = True
    questionVerb = ""
    result = []
    
    for i in xrange(len(tags)):
        (word, tag) = tags[i]
        if (tag in verbTag):
            verbIndex = i
            if (word in beVerb):
                questionVerb = str(word[0].upper() + word[1:])
            else:
                beQuestion = False
                questionVerb = verbTag[tag]
            break

    if (verbIndex != None):
        result.append(questionVerb)
        for i in xrange(verbIndex):
            result.append(text[i])
            
        if (not beQuestion):
            verb = text[verbIndex]
            verb = str(lemmatizer.lemmatize(verb, 'v'))
            result.append(verb)
            
        for i in range(verbIndex+1, len(text)):
            if ((i < len(text)-1) or (i == len(text)-1 and text[i].isalpha())):
                result.append(text[i])
        result.append("?")

    return [" ".join(result)]
            

def whQuestion(text, tags):
    lemmatizer = WordNetLemmatizer()
    verbIndex = None
    beQuestion = True
    questionVerb = ""
    result = []
    
    for i in xrange(len(tags)):
        (word, tag) = tags[i]
        if (tag in verbTag):
            verbIndex = i
            if (word in beVerb):
                questionVerb = str(word[0].upper() + word[1:])
            else:
                beQuestion = False
                questionVerb = verbTag[tag]
            break
        
    result += whoQuestion(text, tags, verbIndex)
    return result

def whoQuestion(text, tags, index):
    question = []
    result = []

    # ne_tags = ne_report(tags)
    
    if (index != None):
        question.append("Who")
            
        for i in range(index, len(text)):
            if ((i < len(text)-1) or (i == len(text)-1 and text[i].isalpha())):
                question.append(text[i])
        question.append("?")
        result.append(" ".join(question))
    return result

def choiceQuestion(text, tags):
    return []


def questionGenerator(sentence):
    result = []
    
    text = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(text)

    result += yesNoQuestion(text, tags)
    result += whQuestion(text, tags)
    result += choiceQuestion(text, tags)

    print result


questionGenerator("Prime Minister Vladimir V. Putin is the country's paramount leader.")
questionGenerator("Prime Minister Vladimir V. Putin returned to Moscow to oversee the federal response.")

questionGenerator("Peter likes to do NLP homework.")
questionGenerator("Peter caught a fish.")
