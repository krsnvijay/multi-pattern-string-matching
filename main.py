import string
import itertools
import matplotlib.pyplot as plt
from nltk.corpus import gutenberg
from nltk.corpus import stopwords
from nltk.corpus import webtext
from nltk.corpus import words
from nltk.corpus import brown

from aho_corasick import test_aho_corasick
from commentz_walter import test_commentz_walter
from corpus import corpus_word_list, randomized_text_patterns, novel_random_text_patterns
from rabin_karp import test_rabin_karp
from synonyms import get_all_patterns

METRICS = {
    'cw': [],
    'ac': [],
    'rk': []
}

INSTANCE_SIZES = [100, 1000, 10000]

ALG_DICT = {
    'cw': 'Commentz-Walter',
    'ac': 'Aho-Corasick',
    'rk': 'Rabin-Karp'
}


def run_algorithms(n=100, m=5, corpus="random"):
    global METRICS
    if corpus == "random":
        print(f"Constructing a random corpus of text with {n} words...")
        search_word_list = corpus_word_list(words.words(), n)
        search_str = ' '.join(search_word_list)
        patterns = randomized_text_patterns(search_word_list, m)

    elif corpus == "gutenburg":
        print(f"Retrieving a corpus of text from a novel having {n} words...")
        tokens = gutenberg.words('austen-emma.txt')
        novel_words = clean_text(tokens)
        # take n sample of words from corpus word list
        search_word_list = corpus_word_list(novel_words, n)  # retrieve from novel
        search_str = ' '.join(corpus_word_list(list(tokens), n))
        # get m sample of words to use as patterns
        patterns = novel_random_text_patterns(search_word_list, m)
    elif corpus == "webtext":
        tokens = webtext.words('firefox.txt')
        webtext_words = clean_text(tokens)
        search_word_list = corpus_word_list(webtext_words, n)  # retrieve from novel
        search_str = ' '.join(corpus_word_list(list(tokens), n))

        # get m sample of words to use as patterns
        patterns = novel_random_text_patterns(search_word_list, m)
    elif corpus == "news":
        tokens = brown.words(categories='news')
        news_text_words = clean_text(tokens)
        search_word_list = corpus_word_list(news_text_words, n)  # retrieve from novel
        search_str = ' '.join(corpus_word_list(list(tokens), n))
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
    print("search string:", search_str)
    METRICS['cw'].append(test_commentz_walter(search_str, patterns)[0])

    print("-" * 20)
    print("\n\n\nBenchmarking AHO-CORASICK")
    print("search string:", search_str)
    METRICS['ac'].append(test_aho_corasick(search_str, patterns)[0])

    print("-" * 20)
    print("\n\n\nBenchmarking RABIN-KARP")
    print("search string:", search_str)
    METRICS['rk'].append(test_rabin_karp(search_str, patterns)[0])
    print("-" * 20)


def clean_text(tokens):
    # convert tokens to lowercase
    tokens = [w.lower() for w in tokens]
    # remove punctuations for words
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # only include words that have alphabets
    cleaned_words = [word for word in stripped if word.isalpha()]
    # remove stop words
    stop_words = set(stopwords.words('english'))
    cleaned_words = [w for w in cleaned_words if not w in stop_words]
    return cleaned_words


def plot_metrics(random_label='Random words', csv_name='result'):
    write_results_csv(csv_name)
    plt.plot(INSTANCE_SIZES, METRICS['cw'], '-o', label="Commentz-Walter", color="chocolate")
    plt.plot(INSTANCE_SIZES, METRICS['ac'], '-o', label="Aho-Corasick", color="green")
    plt.plot(INSTANCE_SIZES, METRICS['rk'], '-o', label="Rabin-Karp", color="blue")
    plt.xlim(0, INSTANCE_SIZES[-1])
    y_limit = int(max(max(METRICS['cw']), max(METRICS['ac']), max(METRICS['rk'])))
    plt.ylim(0, y_limit)
    plt.xticks(range(0, INSTANCE_SIZES[-1] + 2000, 1000))
    plt.yticks(range(0, y_limit + 20, 20))
    plt.title(f"({random_label}) Running times of Commentz-Walter, Aho-Corasick and Rabin-Karp")
    plt.xlabel('Corpus size (in number of words)')
    plt.ylabel('Time (in milliseconds)')
    plt.legend(loc='best')
    print("Wrote results graph to %s.svg" % csv_name)
    plt.savefig('results/%s.svg' % csv_name, bbox_inches='tight',format="svg")
    plt.show()


def write_results_csv(csv_name):
    print("Wrote results to %s.csv" % csv_name)
    with open('results/%s.csv' % csv_name, 'w') as f:
        f.write("ALGORITHM, %s\n" % ', '.join(["%s_WORDS_in_msec" % res_size for res_size in INSTANCE_SIZES]))
        for key in METRICS.keys():
            f.write("%s, %s\n" % (ALG_DICT[key], ', '.join([str(res) for res in METRICS[key]])))
def reset_metrics():
    global METRICS
    METRICS = {
        'cw': [],
        'ac': [],
        'rk': []
    }
if __name__ == "__main__":
    # on a random bag of words
    for instance_size in INSTANCE_SIZES:
        run_algorithms(n=instance_size)
    plot_metrics(csv_name='word_vector_results')
    # on an excerpt from a novel
    # reset metrics

    reset_metrics()
    for instance_size in INSTANCE_SIZES:
        run_algorithms(corpus="gutenburg", n=instance_size)
    plot_metrics(random_label='Novel corpus', csv_name='real_sources_novel_results')
    reset_metrics()
    for instance_size in INSTANCE_SIZES:
        run_algorithms(corpus="news", n=instance_size)
    plot_metrics(random_label='News corpus', csv_name='real_sources_news_results')
    reset_metrics()
    for instance_size in INSTANCE_SIZES:
        run_algorithms(corpus="webtext", n=instance_size)
    plot_metrics(random_label='Webtext corpus', csv_name='real_sources_webtext_results')
