import unittest

from aho_corasick import test_aho_corasick
from commentz_walter import test_commentz_walter
from rabin_karp import test_rabin_karp
from test_data import expected_matches, patterns, search_str, trie_validation_data
from trie import NodeTrie


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.search_str = search_str
        self.patterns = patterns
        self.expected_matches = expected_matches

    def test_ahocorasick(self):
        actual_matches = test_aho_corasick(self.search_str, self.patterns)[1]
        self.assertListEqual(actual_matches, self.expected_matches)

    def test_rabinkarp(self):
        actual_matches = test_rabin_karp(self.search_str, self.patterns)[1]
        self.assertListEqual(actual_matches, self.expected_matches)

    def test_commentz_waltzer(self):
        actual_matches = test_commentz_walter(self.search_str, self.patterns)[1]
        self.assertListEqual(actual_matches, self.expected_matches)

    def test_trie(self):
        trie = NodeTrie()
        for pattern in self.patterns:
            trie.add(pattern)
        print(trie)
        for word, is_valid in trie_validation_data:
            print('testing', word)
            self.assertEqual(trie.has_word(word), is_valid)


if __name__ == '__main__':
    unittest.main()
