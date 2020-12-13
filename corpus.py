import nltk

try:
    nltk.data.find('words')
    nltk.data.find('punkt')
    nltk.data.find('stopwords')
    nltk.data.find('gutenberg')
    nltk.data.find('brown')
    nltk.data.find('webtext')

except:
    nltk.download('words')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('gutenberg')
    nltk.download('brown')
    nltk.download('webtext')

from nltk.corpus import words
from random import sample, randint


def corpus_word_list(corpus_words, n):
    if len(corpus_words) < n:
        n = len(corpus_words)
    if corpus_words is None:
        corpus_words = words.words()
    return sample(corpus_words, n)

def novel_random_text_patterns(word_list,n):
    if len(word_list) < n:
        n = len(word_list)
    from_corpus_number = randint(n // 2, n)
    from_corpus_list = set(corpus_word_list(word_list, from_corpus_number))
    return list(from_corpus_list)

def randomized_text_patterns(word_list, n):
    from_corpus_number = randint(n // 2, n)
    from_corpus_list = set(corpus_word_list(word_list, from_corpus_number))
    another_random_corpus_list = set(corpus_word_list(words.words(), n - from_corpus_number))
    return list(from_corpus_list.union(another_random_corpus_list))
