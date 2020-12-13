from itertools import chain

import nltk
from nltk.corpus import wordnet

from trie import DictTrie

try:
    nltk.data.find('wordnet')
except:
    nltk.download('wordnet')


def get_synonyms(word):
    """
    use wordnet to get synonyms for a particular word
    """
    synonyms = wordnet.synsets(word)
    normal_cased = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    # print(normal_cased)
    return [pattern.lower().replace('_', ' ') for pattern in normal_cased]


def get_all_patterns(search_terms):
    """
    get synonyms for each term in search terms
    """
    all_patterns = set([search_term.lower() for search_term in search_terms])
    for search_term in search_terms:
        all_patterns = all_patterns.union(get_synonyms(search_term))
    return list(all_patterns)


if __name__ == "__main__":
    text = "Privacy is a fundamental human right. At Apple, it’s also one of our key values"
    clean_text = text.replace('[.,]', '')
    words = text.split(" ")
    trie = DictTrie()
    search_word = "fundamental"

    for synonym in get_synonyms(search_word):
        trie.add(synonym)

    print(trie)

    for idx, word in enumerate(words):
        if word in trie:
            print(f"{word} found at {idx}")
