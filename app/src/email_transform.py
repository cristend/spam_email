import urlextract
import re
import nltk
from app.src.spam_classify import email_to_text

url_extractor = urlextract.URLExtract()
stemmer = nltk.PorterStemmer()


class Transformer():
    def __init__(self,
                 strip_headers=True,
                 lower_case=True,
                 remove_punctuation=True,
                 replace_urls=True,
                 replace_numbers=True,
                 stemming=True):
        self.strip_headers = strip_headers
        self.lower_case = lower_case
        self.remove_punctuation = remove_punctuation
        self.replace_urls = replace_urls
        self.replace_numbers = replace_numbers
        self.replace_name = replace_numbers
        self.stemming = stemming

    def transform(self, X):
        text = email_to_text(X) or ''
        if self.lower_case:
            text = text.lower()
        if self.replace_urls and url_extractor is not None:
            urls = list(set(url_extractor.find_urls(text)))
            urls.sort(key=lambda url: len(url), reverse=True)
            for url in urls:
                text = text.replace(url, " URL ")
        if self.replace_numbers:
            text = re.sub(r'\d+(?:\.\d*(?:[eE]\d+))?', 'NUMBER', text)
        if self.remove_punctuation:
            text = re.sub(r'\W+', ' ', text, flags=re.M)
        stemmed_text = ''
        if self.stemming and stemmer is not None:
            for word in text.split():
                stemmed_text += (stemmer.stem(word) + ' ')
            text = stemmed_text
        return text
