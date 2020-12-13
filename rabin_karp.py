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
        calculates the hash value of the given pattern

        :return: int value of the hash
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
            self.hash = int(self.hash/self.base)
            self.hash += ord(self.pattern[self.end]) * self.base ** (self.size - 1)
            self.start += 1
            self.end += 1


def string_matching(text, matcher):
    """
    performs the matching given a text document and list of subs

    :param text: text to match from
    :param matcher: list of patterns to match

    :return: list of indices, if found
    """

    indices = list()
    matcher_set = set()

    # stores length of the pattern. length of all the patterns should be same
    m = len(matcher[0])

    # to store hash values for each string pattern
    for sub in matcher:
        temp = RabinKarp(sub, len(sub))
        matcher_set.add(temp.hash)

    rabin_karp = RabinKarp(text, m)

    # check if the pattern belongs in text
    for i in range(len(text) - m + 1):
        if rabin_karp.hash in matcher_set and text[i:i + m] in matcher:
            indices.append((text[i:i + m], i))
        rabin_karp.rolling_hash()

    return indices


def test_rabin_karp(search_str, patterns):
    print(string_matching(search_str, patterns))

