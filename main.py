import string

from aho_corasick import test_aho_corasick
from commentz_walter import test_commentz_walter
from corpus import corpus_word_list, randomized_text_patterns, novel_random_text_patterns
from rabin_karp import test_rabin_karp
from synonyms import get_all_patterns
import matplotlib.pyplot as plt
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from nltk.corpus import stopwords

METRICS = {
    'cw': [],
    'ac': [],
    'rk': []
}

INSTANCE_SIZES = [100, 1000, 10000]


def run_algorithms(n=100, m=5, random=False):
    global METRICS
    if random:
        print(f"Constructing a random corpus of text with {n} words...")
        search_word_list = corpus_word_list(words.words(), n)
        search_str = ' '.join(search_word_list)
        patterns = randomized_text_patterns(search_word_list, m)

    else:
        print(f"Retrieving a corpus of text from a novel having {n} words...")
        file = open("pride-and-prejudice.txt", 'rt', encoding="utf8")
        novel_text = file.read()
        file.close()
        # convert text to tokens
        tokens = word_tokenize(novel_text)
        # convert tokens to lowercase
        tokens = [w.lower() for w in tokens]
        # remove punctuations for words
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        # only include words that have alphabets
        novel_words = [word for word in stripped if word.isalpha()]
        # remove stop words
        stop_words = set(stopwords.words('english'))
        novel_words = [w for w in novel_words if not w in stop_words]
        # take n sample of words from corpus word list
        search_word_list = corpus_word_list(novel_words, n)  # retrieve from novel
        search_str = ' '.join(search_word_list)
        # get m sample of words to use as patterns
        patterns = novel_random_text_patterns(search_word_list, m)

    before_syn_num = len(patterns)
    print("Number of patterns before getting synonyms: ", before_syn_num)
    print(patterns)
    patterns = get_all_patterns(patterns)
    print(
        f"{len(patterns) - before_syn_num} synonym patterns were added.\nTotally {len(patterns)} are going to be searched for.")
    print(patterns)

    # call algorithms
    print("-" * 20)
    print("\n\n\nBenchmarking COMMENTZ-WALTER")
    METRICS['cw'].append(test_commentz_walter(search_str, patterns))

    print("-" * 20)
    print("\n\n\nBenchmarking AHO-CORASICK")
    METRICS['ac'].append(test_aho_corasick(search_str, patterns))

    print("-" * 20)
    print("\n\n\nBenchmarking RABIN-KARP")
    METRICS['rk'].append(test_rabin_karp(search_str, patterns))
    print("-" * 20)


def plot_metrics(random_label='Random words'):
    plt.plot(INSTANCE_SIZES, METRICS['cw'], '-o', label="Commentz-Walter", color="chocolate")
    plt.plot(INSTANCE_SIZES, METRICS['ac'], '-o', label="Aho-Corasick", color="green")
    plt.plot(INSTANCE_SIZES, METRICS['rk'], '-o', label="Rabin-Karp", color="blue")
    plt.xlim(0, INSTANCE_SIZES[-1])
    y_limit = int(max(max(METRICS['cw']), max(METRICS['ac']), max(METRICS['rk'])))
    plt.ylim(0, y_limit)
    plt.xticks(range(0, INSTANCE_SIZES[-1] + 2000, 1000))
    plt.yticks(range(0, y_limit + 20, 10))
    plt.title(f"({random_label}) Running times of Commentz-Walter, Aho-Corasick and Rabin-Karp")
    plt.xlabel('Corpus size (in number of words)')
    plt.ylabel('Time (in milliseconds)')
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    # on a random bag of words
    for instance_size in INSTANCE_SIZES:
        run_algorithms(n=instance_size)
    plot_metrics()
    # on an excerpt from a novel
    for instance_size in INSTANCE_SIZES:
        run_algorithms(n=instance_size)
    plot_metrics(random_label='Novel corpus')
