import nltk
import string

class WordOnlyTokenizer:
    def tokenize(self, text):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        stem = nltk.stem.SnowballStemmer('english')
        text = text.lower()

        for token in nltk.word_tokenize(text):
            if (token in string.punctuation) or (token in string.digits): continue
            yield stem.stem(token)