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

# store running time for each algorithm based on their instance size
METRICS = {
    'cw': [],
    'ac': [],
    'rk': []
}

THEORETICAL_METRICS = {
    'cw': [],
    'ac': [],
    'rk': []
}

# no of words that can be present in a search_string
INSTANCE_SIZES = [100, 1000, 10000]

ALG_DICT = {
    'cw': 'Commentz-Walter',
    'ac': 'Aho-Corasick',
    'rk': 'Rabin-Karp'
}


def run_algorithms(n=100, m=5, corpus="random"):
    """
    Benchmark all algorithms for 'n' instance size, and 'm' patterns
     using a corpus that is either random|book|webtext|news
     """
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
    THEORETICAL_METRICS['cw'].append((len(search_str) * len(max(patterns, key=len))) / 1000)  # O(mn)

    print("-" * 20)
    print("\n\n\nBenchmarking AHO-CORASICK")
    print("search string:", search_str)
    ac_metrics = test_aho_corasick(search_str, patterns)
    METRICS['ac'].append(ac_metrics[0])
    THEORETICAL_METRICS['ac'].append((
                                             len(search_str) + ac_metrics[0] + sum(
                                         len(pattern) for pattern in patterns)) / 1000)  # O(n + m + k)

    print("-" * 20)
    print("\n\n\nBenchmarking RABIN-KARP")
    print("search string:", search_str)
    METRICS['rk'].append(test_rabin_karp(search_str, patterns)[0])
    print("-" * 20)
    THEORETICAL_METRICS['rk'].append((len(search_str)*m + len(min(patterns, key=len))) / 1000)  # O(nm + k)


def clean_text(tokens):
    """
    Preprocess words of a text to force lowercase conversion,remove punctuations,
     remove numbers and remove stop words
     """
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
    """
    Plot a multiline graph using metrics for each algorithm on all input sizes,
     and export the graph to an output file
     """
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
    plt.savefig('results/%s.svg' % csv_name, bbox_inches='tight', format="svg")
    plt.clf()
    plt.close()


def write_results_csv(csv_name):
    """
    Create and write the metrics for the current run to a csv file
    """
    print("Wrote results to %s.csv" % csv_name)
    with open('results/%s.csv' % csv_name, 'w') as f:
        f.write("ALGORITHM, %s\n" % ', '.join(["%s_WORDS_in_msec" % res_size for res_size in INSTANCE_SIZES]))
        for key in METRICS.keys():
            f.write("%s, %s\n" % (ALG_DICT[key], ', '.join([str(res) for res in METRICS[key]])))


def reset_metrics():
    """
    Reset metrics when running the benchmark with different corpus type
    """
    global METRICS
    METRICS = {
        'cw': [],
        'ac': [],
        'rk': []
    }


def plot_comparison_metrics(alg):
    plt.plot(INSTANCE_SIZES, METRICS[alg], '-o', label=f"Experimental {ALG_DICT[alg]}", color="blue")
    plt.plot(INSTANCE_SIZES, THEORETICAL_METRICS[alg], '--bo', label=f"Theoretical {ALG_DICT[alg]}", color="red")
    plt.xlim(0, INSTANCE_SIZES[-1])
    y_limit = int(max(max(METRICS[alg]), max(THEORETICAL_METRICS[alg])))
    plt.ylim(0, y_limit)
    plt.xticks(range(0, INSTANCE_SIZES[-1] + 2000, 1000))
    if alg == 'ac':
        plt.yticks(range(0, y_limit + 20, 20))
    plt.title(f"{ALG_DICT[alg]} Theoretical guarantee vs Experimental running time")
    plt.xlabel('Corpus size (in number of words)')
    plt.ylabel('Time (in milliseconds)')
    plt.legend(loc='best')
    print("Wrote results graph to %s.svg" % f"theoretical_cmp_{alg}")
    plt.savefig('results/%s.svg' % f"theoretical_cmp_{alg}", bbox_inches='tight', format="svg")
    plt.clf()
    plt.close()


if __name__ == "__main__":
    # on a random bag of words
    for instance_size in INSTANCE_SIZES:
        run_algorithms(n=instance_size)
    plot_metrics(csv_name='word_vector_results')
    plot_comparison_metrics('ac')
    plot_comparison_metrics('cw')
    plot_comparison_metrics('rk')
    # on an excerpt from a novel
    # reset metrics

    reset_metrics()
    # run benchmark on a jane-austen novel
    for instance_size in INSTANCE_SIZES:
        run_algorithms(corpus="gutenburg", n=instance_size)
    plot_metrics(random_label='Novel corpus', csv_name='real_sources_novel_results')
    reset_metrics()
    # run benchmark on a news corpus
    for instance_size in INSTANCE_SIZES:
        run_algorithms(corpus="news", n=instance_size)
    plot_metrics(random_label='News corpus', csv_name='real_sources_news_results')
    reset_metrics()
    # run benchmark on a web text corpus
    for instance_size in INSTANCE_SIZES:
        run_algorithms(corpus="webtext", n=instance_size)
    plot_metrics(random_label='Webtext corpus', csv_name='real_sources_webtext_results')
