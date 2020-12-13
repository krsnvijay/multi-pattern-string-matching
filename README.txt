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


1. Running the project locally
-------------------

# Using poetry
Install poetry from (https://python-poetry.org/docs/#installation)
which is a tool for dependency management and packaging in Python
> poetry install

# Using pip
You can also install dependencies to your python environment
> pip install -r requirements.txt

2. Run algorithms
-------------------
main.py bench marks Rabin Karp, Commentz Walter, Aho Corasick
using corpus from Wordnet, Webtext, Gutenberg, News downloadable from nltk library
The generated graphs will be saved to the results directory

# Using poetry
> poetry run python main.py

# Using your venv
> python main.py

3. Run unit tests
-------------------
Unit tests, check if each of the algorithm returns the right matches
with the search string and patterns provided to it

# Using poetry
> poetry run python -m unittest

# Using pip
> python -m unittest

