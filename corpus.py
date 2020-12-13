import nltk

try:
    nltk.data.find('words')
except:
    nltk.download('words')

from nltk.corpus import words
from random import sample, randint


def corpus_word_list(n):
    return sample(words.words(), n)


def randomized_text_patterns(word_list, n):
    from_corpus_number = randint(n // 2, n)
    from_corpus_list = set(sample(word_list, from_corpus_number))
    another_random_corpus_list = set(sample(words.words(), n - from_corpus_number))
    return list(from_corpus_list.union(another_random_corpus_list))
