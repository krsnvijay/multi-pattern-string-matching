from trie import NodeTrie
from collections import deque
import time


class AhoCorasick(NodeTrie):
    """
    Aho Corasick implementation that uses NodeTrie as its base class
    """

    def create_failure_links(self):
        """
        construct a finite state machine by creating
        failure links between  trie nodes for faster transition
        """
        fifo_queue = deque()

        # Add failure link for children of root
        for letter in self.children:
            child = self.children[letter]
            child.failure_link = self

            # Add children of root node to bfs
            for nested_letter in child.children:
                nested_child = child.children[nested_letter]
                fifo_queue.append(nested_child)

        # traverse through all nodes of a trie and add failure links using BFS
        while fifo_queue:
            corasick_node = fifo_queue.popleft()
            # Add children of the node to queue that is currently being processed
            for letter in corasick_node.children:
                child = corasick_node.children[letter]
                fifo_queue.append(child)

            # Get longest matching suffix as failure link
            corasick_node.failure_link = corasick_node.get_failure_link()
            # if failure link is a word, then make the current link a dictionary link, support substring matching
            failure_link_is_word = corasick_node.failure_link.word is not None
            corasick_node.dictionary_link = corasick_node.failure_link if failure_link_is_word else corasick_node.failure_link.dictionary_link

    def find_all_matches(self, text):
        """
        Traverse through the finite state machine following failure links and trie nodes to find substring_matches if any exist
        """
        substring_matches = deque()
        # forcing trie to be case insensitive
        text = text.lower()
        position = 0
        corasick_node = self
        for letter in text:
            # traverse the trie if letter exists as a child
            if letter in corasick_node:
                corasick_node = corasick_node.children[letter]
            else:
                # traverse the failure link of the trie
                while not corasick_node.is_root():
                    corasick_node = corasick_node.failure_link
                    if letter in corasick_node:
                        corasick_node = corasick_node.children[letter]
                        break

            # if corasick_node is a word node add it as a match
            if corasick_node.word is not None:
                substring_matches.append((corasick_node.word, position - len(corasick_node.word) + 1))

            output_searcher = corasick_node.dictionary_link
            # if there is a substring that substring_matches
            while output_searcher is not None:
                substring_matches.append((output_searcher.word, position - len(output_searcher.word) + 1))
                output_searcher = output_searcher.dictionary_link
            position += 1
        return substring_matches


def test_aho_corasick(search_str, patterns, test_trie=False):
    """
    Builds a trie with patterns and runs aho corasick algorithm on the search string
    """
    aho_corasick = AhoCorasick()
    for pattern in patterns:
        aho_corasick.add(pattern)

    print("\nTrie: Created")
    print(aho_corasick)

    if test_trie:
        test_patterns = ["Hi", "Hit", "No", "North", "Yes"]
        print(f"\nTrie: Testing Patterns")
        for test_pattern in test_patterns:
            print((test_pattern, aho_corasick.has_word(test_pattern)))

    print("\nCreating failure links")
    start_time = time.perf_counter()
    aho_corasick.create_failure_links()
    matches = aho_corasick.find_all_matches(search_str)
    end_time = time.perf_counter()
    print(f'\nSearch for multi-patterns in a string of length {len(search_str)}')
    print(f"Matches: {len(matches)} found in {end_time - start_time:0.8f} second(s)")

    for match in matches:
        # print((match[1] - 2)*' ',match)
        print(match)
    return (end_time - start_time) * 10 ** 3, list(matches)
