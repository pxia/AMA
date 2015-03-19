import nltk
import util
from collections import Counter

class Article(object):
    def __init__(self, text):
        super(Article, self).__init__()
        self.text = text
        self.tagged = [nltk.pos_tag(nltk.word_tokenize(s))
            for s in nltk.sent_tokenize(text)]

    def sentencesContainsKeywords(self, kws):
        """"""
        sentences = Counter()
        for i in xrange(len(self.tagged)):
            score = 0
            for kw in kws:
                if util.pos_tagContains(self.tagged[i], kw):
                    score += len(kw)
            if (score == 0): break
            sentences[i] = score
        return map(lambda (i, s): (self.tagged[i], s), sentences.most_common())

    def answer(self, question):
        kws = extractKws(pos_tag(question))
        releventSent = self.sentencesContainsKeywords(kws)

if __name__ == '__main__':
    a = Article("this's a sent tokenize test. this is sent two. is this sent three? sent 4 is cool! Now it's your turn.")
    print a.sentencesContainsKeywords([['sent', 'tokenize']])
