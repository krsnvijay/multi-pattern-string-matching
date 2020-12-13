search_str = 'Mozilla Firefox, or simply Firefox, is a free and open-source web browser developed by the Mozilla Foundation and its subsidiary, the Mozilla Corporation. Firefox uses the Gecko layout engine to render web pages, which implements current and anticipated web standards.'

# Add synonyms for some words and some words that don't exist
patterns = ['render', 'open-source', 'free', 'paid', 'advertisements']

trie_validation_data = [('opens', False), ('ads', False), ('free', True), ('render', True)]
expected_matches = [
    ('free', 41),
    ('open-source', 50),
    ('render', 195)
]
