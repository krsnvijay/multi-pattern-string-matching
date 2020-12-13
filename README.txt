Quick Start
-------------------
1.Install dependencies using
    > pip install -r requirements.txt
2.Benchmark algorithms using
    > python main.py
3.Check results directory to check the graphs, running time from benchmark
4.Run unittests (optional)
    > python -m unittest

Directory structure
-------------------
    .
    ├── results                 # Contains graphs,running time generated from benchmarks
    ├── main.py                 # Benchmarks all algorithms
    ├── aho_corasick.py         # Aho Corasick implementation
    ├── commentz_walter.py      # Commentz Walter implementation
    ├── rabin_karp.py           # Rabin Karp implementation
    ├── trie.py                 # Contains trie implementation
    ├── corpus.py               # Downloads corpus from nltk and takes samples
    ├── synonyms.py             # Gets synonyms for words from nltk
    ├── test_algorithms.py      # Contains unit test class for all algorithms and trie
    ├── test_data.py            # Contains data that is used as setup for each test case
    ├── requirements.txt        # Dependencies to be installed using pip
    ├── pyproject.toml          # Poetry's dependency management file
    └── README.md

Libraries used
-------------------
matplotlib==3.3.3 (https://matplotlib.org/)
nltk==3.5 (https://www.nltk.org/)

Corpus used for benchmark
-------------------
1. WordNet (https://wordnet.princeton.edu/)
2. Brown Corpus (http://korpus.uib.no/icame/brown/bcm.html) - "News" category
3. Web Text Corpus (http://www.nltk.org/nltk_data/) - file-id "firefox.txt"
4. Project Gutenberg Selections (http://www.nltk.org/nltk_data/) - file-id "austen-emma.txt"