import time
from collections import deque


class RabinKarp:
    """
    class to implement Rabin-Karp Algorithm
    """

    def __init__(self, pattern, size):
        self.pattern = pattern
        self.size = size
        self.base = 3
        self.hash = self.hash_pattern()
        self.start = 0
        self.end = size

    def hash_pattern(self):
        """
        calculates and returns the hash value of the given pattern
        """
        total = 0
        y = [ord(x) for x in list(self.pattern)]
        for i in range(self.size):
            total += y[i] * self.base ** i
        return total

    def rolling_hash(self):
        """
        method to compute the next hash value from the previous hash value
        helps in reducing the complexity from O(mn) to O(m+n)
        where m is the size of string to match and n is the size of text
        """
        if self.end < len(self.pattern):
            self.hash -= ord(self.pattern[self.start])
            self.hash = int(self.hash / self.base)
            self.hash += ord(self.pattern[self.end]) * self.base ** (self.size - 1)
            self.start += 1
            self.end += 1


def string_matching(text, matcher):
    """
    finds and returns the substring_matches given a text document and list of patterns to match
    """

    substring_matches = deque()
    matcher_set = dict()

    # stores length of the pattern. length of all the patterns should be same
    m = min([len(x) for x in matcher])

    # to store hash values for each string pattern
    for sub in matcher:
        temp = RabinKarp(sub, m)
        matcher_set[sub] = temp.hash

    text_obj = RabinKarp(text.lower(), m)

    # check if the pattern belongs in text
    for i in range(len(text) - m + 1):
        if text_obj.hash in matcher_set.values():
            for pat in matcher:
                if text[i: i + len(pat)].lower() == pat:
                    substring_matches.append((text[i: i + len(pat)], i))
        text_obj.rolling_hash()

    return substring_matches


def test_rabin_karp(search_str, patterns):
    start_time = time.perf_counter()
    match_tuples = string_matching(search_str, patterns)
    end_time = time.perf_counter()
    print(f'\nSearch for multi-patterns in a string of length {len(search_str)}')
    print(f"Matches: {len(match_tuples)} found in {end_time - start_time:0.8f} second(s)")
    for match_tuple in match_tuples:
        print(match_tuple)
    return (end_time - start_time) * 10 ** 3, list(match_tuples)
