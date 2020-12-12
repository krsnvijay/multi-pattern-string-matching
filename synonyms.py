from wn import WordNet
from trie import DictTrie
from itertools import chain


def get_synonyms(word):
    wordnet = WordNet()
    synonyms = wordnet.synsets(word)
    return chain.from_iterable([word.lemma_names() for word in synonyms])


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

