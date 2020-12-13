# Multi Pattern String Matching Algorithms

## Introduction
In our project, we aim to carry out worst-case analyses of various multi-pattern string matching
algorithms by implementing and running them on various input instances. For our problem statement,

We consider a synonym-inclusive string search: given a search query and a corpus to search in, we
search for occurrences of each word in the search query with its synonyms from a dataset like
WordNet. We can then observe how the performance of state-of-the-art multi-pattern string matching
algorithms compares against their theoretical guarantees.

![patter matching](images/fig1.png)

For this,  we  chose  three  state  of  the  art  algorithms  to  study,  analyze,  implement,  and  compare.Each algorithm is implemented in Python.  The three algorithms under consideration are:
1.  Aho-Corasick algorithm (an extension of Knuth-Morris-Pratt algorithm)
2.  Commentz-Walter algorithm (an extension of Boyer-Moore algorithm)
3.  Rabin-Karp algorithm

## Running the project locally

### Directory structure
    .
    ├── results                 # Contains graphs,running time generated from benchmarks 
    ├── aho_corasick.py         # Aho Corasick implementation
    ├── commentz_walter.py      # Commentz Walter implementation
    ├── rabin_karp.py           # Rabin Karp implementation
    ├── main.py                 # Benchmarks all algorithms
    ├── trie.py                 # Contains trie implementation
    ├── corpus.py               # Downloads corpus from nltk and takes samples
    ├── synonyms.py             # Gets synonyms for words from nltk
    ├── test_algorithms.py      # Contains unit test class for all algorithms and trie
    ├── test_data.py            # Contains data that is used as setup for each test case
    ├── requirements.txt        # Dependencies to be installed using pip
    ├── pyproject.toml          # Poetry's dependency management file
    └── README.md
### Installing requirements

```
matplotlib==3.3.3
nltk==3.5
```


#### Using poetry
Install [poetry](https://python-poetry.org/docs/#installation) which is a tool for dependency management and packaging in Python
```bash
poetry install
```
#### Using pip
You can also install dependencies to your python environment
```bash
pip install -r requirements.txt
```
### Run algorithms
 ```main.py``` bench marks Rabin Karp, Commentz Walter, Aho Corasick using corpus from [Wordnet, Webtext, Gutenberg, News](http://www.nltk.org/nltk_data/) that is downloadable with the [nltk library](https://www.nltk.org/).

#### Using poetry

```bash
poetry run python main.py
```
#### Using your venv
```bash
python main.py
```
### Run unit tests
Unit tests, check if each of the algorithm returns the right matches with the search string and patterns provided to it
#### Using poetry
```bash
poetry run python -m unittest
```
#### Using pip
```bash
python -m unittest
```

## Results
1. [WordNet](https://wordnet.princeton.edu/)
![Word Vector](results/word_vector_results.svg)

2. [Brown Corpus](http://korpus.uib.no/icame/brown/bcm.html) - "News" category
![News Corpus](results/real_sources_news_results.svg)

3. [Web Text Corpus](http://www.nltk.org/nltk_data/) - file-id "firefox.txt"
![Webtext Corpus](results/real_sources_webtext_results.svg)

4. [Project Gutenberg Selections](http://www.nltk.org/nltk_data/) - file-id "austen-emma.txt"
![Novel Corpus](results/real_sources_novel_results.svg)
