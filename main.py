from aho_corasick import test_aho_corasick
from commentz_walter import test_commentz_walter
from corpus import corpus_word_list, randomized_text_patterns
from synonyms import get_all_patterns


def run_algorithms(n=100, m=5):
    print(f"Constructing a random corpus of text with {n} words...")
    search_word_list = corpus_word_list(n)  # text corpus
    search_str = ' '.join(search_word_list)

    patterns = randomized_text_patterns(search_word_list, m)
    before_syn_num = len(patterns)
    print("Number of patterns before getting synonyms: ", before_syn_num)
    print(patterns)
    patterns = get_all_patterns(patterns)
    print(f"{len(patterns) - before_syn_num} synonym patterns were added.\nTotally {len(patterns)} are going to be searched for.")
    print(patterns)

    # call algorithms
    print("-"*20)
    print("\n\n\nBenchmarking COMMENTZ-WALTER")
    test_commentz_walter(search_str, patterns)
    print("-" * 20)
    print("\n\n\nBenchmarking AHO-CORASICK")
    test_aho_corasick(search_str, patterns)
    print("-" * 20)

if __name__ == "__main__":
    run_algorithms()
