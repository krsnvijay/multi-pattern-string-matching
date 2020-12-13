from synonyms import get_all_patterns
from trie import NodeTrie
from collections import deque
import time

class AhoCorasick(NodeTrie):

    def create_failure_links(self):
        bfs_queue = deque()

        # Add failure link for children of root
        for letter in self.children:
            child = self.children[letter]
            child.failure_link = self

            # Add children of root node to bfs
            for nested_letter in child.children:
                grand_child = child.children[nested_letter]
                bfs_queue.append(grand_child)

        # traverse through all nodes of a trie and add failure links using BFS
        while len(bfs_queue) > 0:
            current_node = bfs_queue.popleft()
            # Add children of the node to queue that is currently being processed
            for key in current_node.children:
                child = current_node.children[key]
                bfs_queue.append(child)

            # Get longest matching suffix as failure link
            current_node.failure_link = current_node.get_failure_link()
            # if failure link is a word, then make the current link a dictionary link, support substring matching
            suffix_is_word = current_node.failure_link.word is not None
            current_node.dictionary_link = current_node.failure_link if suffix_is_word else current_node.failure_link.dictionary_link

    def find_all_matches(self, text):
        matches = deque()
        text = text.lower()
        pos = 0
        current_node = self
        for letter in text:
            # traverse the trie if letter exists as a child
            if letter in current_node:
                current_node = current_node.children[letter]
            else:
                # traverse the failure link of the trie
                while not current_node.is_root():
                    current_node = current_node.failure_link
                    if letter in current_node:
                        current_node = current_node.children[letter]
                        break

            # if current_node is a word node add it as a match
            if current_node.word is not None:
                matches.append((current_node.word, pos - len(current_node.word) + 1))

            output_searcher = current_node.dictionary_link
            # if there is a substring that matches
            while output_searcher is not None:
                matches.append((output_searcher.word, pos - len(output_searcher.word) + 1))
                output_searcher = output_searcher.dictionary_link
            pos += 1
        return matches


def test_aho_corasick(search_str, patterns, test_trie=False):
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
