import time

from corpus import corpus_word_list, randomized_text_patterns
from trie import NodeTrie
from collections import deque
from synonyms import get_all_patterns


class CommentzWalter(NodeTrie):
    def add_word(self, word):
        word = word[::-1]
        super().add(word)
        pos = 1

        # Initialize character table
        for character in word:
            min_char_depth = self.char_lookup_table.get(character)
            if (min_char_depth is None) or (min_char_depth > pos):
                self.char_lookup_table[character] = pos
            pos += 1

        if self.min_depth is None:
            self.min_depth = len(word)
        elif len(word) < self.min_depth:
            self.min_depth = len(word)

    def has_word(self, word):
        word = word[::-1]
        return super().has_word(word)

    def initialize_shift_values(self):
        bfs_queue = deque()
        self.shift1 = 1
        self.shift2 = self.min_depth

        for key in self.children:
            bfs_queue.append(self.children[key])

        while (len(bfs_queue) > 0):
            current_node = bfs_queue.popleft()
            # set shift1
            if current_node.CWsuffix_link is None:
                current_node.shift1 = self.min_depth
            else:
                current_node.shift1 = current_node.min_difference_s1

            # set shift2
            if current_node.CWoutput_link is None:
                current_node.shift2 = current_node.parent.shift2
            else:
                current_node.shift2 = current_node.min_difference_s2

            for key in current_node.children:
                bfs_queue.append(current_node.children[key])

    def create_failure_links(self):
        bfs_queue = deque()

        # First, set suffix links for first children to root
        for key in self.children:
            child = self.children[key]
            child.failure_link = self

            for key2 in child.children:
                grandchild = child.children[key2]
                bfs_queue.append(grandchild)

        while (len(bfs_queue) > 0):
            current_node = bfs_queue.popleft()
            for key in current_node.children:
                child = current_node.children[key]
                bfs_queue.append(child)

            # Set AC nodes first
            AC_suffix_node = current_node.get_failure_link()
            current_node.failure_link = AC_suffix_node
            suffix_is_word = current_node.failure_link.word is not None
            current_node.dictionary_link = current_node.failure_link if suffix_is_word else current_node.failure_link.dictionary_link
            if current_node.dictionary_link is not None:
                pass

            # Set reverse suffix links and output links
            is_set2 = current_node.word is not None
            if AC_suffix_node.min_difference_s1 == -1 or AC_suffix_node.min_difference_s1 > current_node.depth - AC_suffix_node.depth:
                AC_suffix_node.min_difference_s1 = current_node.depth - AC_suffix_node.depth
                AC_suffix_node.CWsuffix_link = current_node
            if is_set2:
                if AC_suffix_node.min_difference_s2 == -1 or AC_suffix_node.min_difference_s2 > current_node.depth - AC_suffix_node.depth:
                    AC_suffix_node.min_difference_s2 = current_node.depth - AC_suffix_node.depth
                    AC_suffix_node.CWoutput_link = current_node

        self.initialize_shift_values()

    def char_func(self, character):
        min_depth = self.char_lookup_table.get(character)
        if min_depth is None:
            min_depth = self.min_depth + 1

        return min_depth

    def shift_func(self, node, j):
        max_of_s1_and_char = 0
        if node.letter is None:
            max_of_s1_and_char = node.shift1
        else:
            max_of_s1_and_char = max(self.char_func(node.letter) - j - 1, node.shift1)
        return min(max_of_s1_and_char, node.shift2)

    def find_all_matches(self, text):
        i = self.min_depth - 1
        text = text.lower()
        matches = deque()

        while i < len(text):
            # Scan Phase
            v = self
            j = 0
            char_to_find = text[i - j]
            while (char_to_find in v) and (i - j >= 0):
                v = v.children[char_to_find]
                j += 1

                if v.word is not None:
                    matches.append((v.word[::-1], i - j + 1))

                char_to_find = text[i - j]

            if j > i:
                j = i

            i += self.shift_func(v, j)

        return matches


def test_commentz_walter(search_str, patterns, test_trie=False):
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
    return (end_time-start_time)*10**3, list(matches)
