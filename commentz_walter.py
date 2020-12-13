import time
from trie import NodeTrie
from collections import deque


class CommentzWalter(NodeTrie):
    """
    Commentz Walter implementation that uses NodeTrie as its base class
    """

    def add_word(self, word):
        """
        Reverse the word and add it to the node trie
        """
        word = word[::-1]
        super().add(word)
        position = 1

        # Initialize letter table for the letters of the word
        for letter in word:
            min_letter_depth = self.letter_lookup_table.get(letter)
            if (min_letter_depth is None) or (min_letter_depth > position):
                self.letter_lookup_table[letter] = position
            position += 1

        if self.min_depth is None:
            self.min_depth = len(word)
        elif len(word) < self.min_depth:
            self.min_depth = len(word)

    def has_word(self, word):
        """
        Override NodeTrie's has_word to use the reverse of that node for performing a lookup
        """
        word = word[::-1]
        return super().has_word(word)

    def set_shift_values(self):
        fifo_queue = deque()
        self.s1 = 1
        self.s2 = self.min_depth

        # use bfs to traverse through all children nodes
        for letter in self.children:
            fifo_queue.append(self.children[letter])

        while fifo_queue:
            walter_node = fifo_queue.popleft()
            # set shift1
            if walter_node.failure_link_cw is None:
                walter_node.s1 = self.min_depth
            else:
                walter_node.s1 = walter_node.min_diff_s1

            # set shift2
            if walter_node.dictionary_link_cw is None:
                walter_node.s2 = walter_node.parent.s2
            else:
                walter_node.s2 = walter_node.min_diff_s2

            for letter in walter_node.children:
                fifo_queue.append(walter_node.children[letter])

    def create_failure_links(self):
        """
        construct a finite state machine by creating
        failure links between trie nodes for faster transition similar to ahocorasick
        set shift values for comment waltzer
        """
        fifo_queue = deque()

        # perform bfs from the root of the trie and set their failure links
        for letter in self.children:
            child = self.children[letter]
            child.failure_link = self

            for nested_letter in child.children:
                nested_child = child.children[nested_letter]
                fifo_queue.append(nested_child)

        while fifo_queue:
            walter_node = fifo_queue.popleft()
            for letter in walter_node.children:
                child = walter_node.children[letter]
                fifo_queue.append(child)

            # set failure links for walter_node similar to aho corasick
            suffix_node = walter_node.get_failure_link()
            walter_node.failure_link = suffix_node
            failure_link_is_word = walter_node.failure_link.word is not None
            walter_node.dictionary_link = walter_node.failure_link if failure_link_is_word else walter_node.failure_link.dictionary_link
            if walter_node.dictionary_link is not None:
                pass

            # Set reverse failure links and dictionary links for walter_node
            walter_suffix_diff = walter_node.depth - suffix_node.depth
            is_set2 = walter_node.word is not None
            if suffix_node.min_diff_s1 == -1 or suffix_node.min_diff_s1 > walter_suffix_diff:
                suffix_node.min_diff_s1 = walter_suffix_diff
                suffix_node.failure_link_cw = walter_node
            if is_set2:
                if suffix_node.min_diff_s2 == -1 or suffix_node.min_diff_s2 > walter_suffix_diff:
                    suffix_node.min_diff_s2 = walter_suffix_diff
                    suffix_node.dictionary_link_cw = walter_node

        # initialize shift values
        self.set_shift_values()

    def get_letter_min_depth(self, letter):
        """
        Use lookup table to get the letter's min depth
        """
        min_depth = self.letter_lookup_table.get(letter)
        if min_depth is None:
            min_depth = self.min_depth + 1

        return min_depth

    def get_walter_node_shift(self, walter_node, j):
        """
        get shift value of a cw node from position depth j
        """
        if walter_node.letter is None:
            max_of_s1_and_letter = walter_node.s1
        else:
            max_of_s1_and_letter = max(self.get_letter_min_depth(walter_node.letter) - j - 1, walter_node.s1)
        return min(max_of_s1_and_letter, walter_node.s2)

    def find_all_matches(self, text):
        """
        Traverse through the trie nodes to find substring_matches if any exist
        """
        idx = self.min_depth - 1
        text = text.lower()
        substring_matches = deque()

        while idx < len(text):
            # start from the root
            walter_node = self
            j = 0
            search_letter = text[idx - j]
            while (search_letter in walter_node) and (idx - j >= 0):
                walter_node = walter_node.children[search_letter]
                j += 1
                if walter_node.word is not None:
                    substring_matches.append((walter_node.word[::-1], idx - j + 1))

                search_letter = text[idx - j]

            if j > idx:
                j = idx

            idx += self.get_walter_node_shift(walter_node, j)

        return substring_matches


def test_commentz_walter(search_str, patterns, test_trie=False):
    """
    Builds a trie with patterns and runs commentz walter algorithm on the search string
    """
    commentz_walter = CommentzWalter()
    for pattern in patterns:
        commentz_walter.add_word(pattern)

    print("\nTrie: Created")
    print(commentz_walter)

    if test_trie:
        test_patterns = ["Hi", "Hit", "No", "North", "Yesn't"]
        print(f"\nTrie: Testing Patterns")
        for test_pattern in test_patterns:
            print((test_pattern, commentz_walter.has_word(test_pattern)))

    print("\nCreating failure links")
    start_time = time.perf_counter()
    commentz_walter.create_failure_links()
    matches = commentz_walter.find_all_matches(search_str)
    end_time = time.perf_counter()

    print(f'\nSearch for multi-patterns in a string of length {len(search_str)}')
    print(f"Matches: {len(matches)} found in {end_time - start_time:0.8f} second(s)")

    for match in matches:
        # print((match[1] - 2) * ' ', match)
        print(match)
    return (end_time - start_time) * 10 ** 3, list(matches)
