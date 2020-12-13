import pprint


class NodeTrie:
    """
    Implementation of trie using nodes,
    where each node stores a letter and also has a dictionary of its child nodes
    """

    def __init__(self, letter=None, parent=None, depth=0):
        """Constructor for a root trie node"""
        # variables needed for trie node
        self.letter = letter
        self.parent = parent
        self.word = None
        self.children = {}
        # variables needed for corasick node
        self.failure_link = None
        self.dictionary_link = None
        # variables needed for walter node
        self.size = 0
        self.depth = depth
        self.failure_link_cw = None
        self.dictionary_link_cw = None
        self.min_diff_s1 = -1
        self.min_diff_s2 = -1
        self.min_depth = None
        self.letter_lookup_table = {}

    def add(self, word):
        """
        Add a word to the trie
        """
        cur_trie_node = self
        cur_depth = self.depth + 1
        for letter in word:
            if letter not in cur_trie_node.children:
                nxt_node = NodeTrie(letter, cur_trie_node, cur_depth)
                cur_trie_node.children[letter] = nxt_node
            else:
                nxt_node = cur_trie_node.children[letter]
            cur_trie_node = nxt_node
            cur_depth += 1

        if cur_trie_node.word is not None:
            return

        cur_trie_node.word = word
        self.size += 1

    def has_word(self, word):
        """
        Check if a word exists in the trie by traversing through its children from the root
        """
        cur_trie_node = self
        word = word.lower()
        for letter in word:
            if letter not in cur_trie_node.children:
                return False
            cur_trie_node = cur_trie_node.children[letter]
        return True

    def is_root(self):
        """
        check if the current node is a root
        """
        return self.letter is None

    def __contains__(self, letter):
        """
        check if the current node has a child with the key letter
        """
        return letter in self.children

    def __str__(self):
        """
        return string representation of the tries children
        """
        return pprint.pformat(self.children, indent=1, compact=True)

    def __repr__(self):
        """
        return string representation of the tries grand children
        """
        return pprint.pformat(self.children, indent=1, compact=True)

    def __len__(self):
        """
        return no of word|patterns in the trie
        """
        return self.size

    def get_failure_link(self):
        """
        get longest suffix match of the current node
        """
        longest_suffix_matcher = self.parent.failure_link
        # find a matching suffix by traversing its children and failure links
        while (not longest_suffix_matcher.is_root()) and (self.letter not in longest_suffix_matcher):
            longest_suffix_matcher = longest_suffix_matcher.failure_link

        if self.letter in longest_suffix_matcher:
            return longest_suffix_matcher.children[self.letter]
        else:
            if not longest_suffix_matcher.is_root():
                print("incorrect failure links creation")
            return longest_suffix_matcher


class DictTrie:
    """
    Trie implentation using dictionaries
    """

    def __init__(self):
        """
        Constructor for Trie with a dictionary as its root node
        """
        self.root = {'*': '*'}

    def add(self, word):
        """
        Add a word to the trie
        """
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                current_node[letter] = {}
            current_node = current_node[letter]
        current_node['*'] = '*'

    def __contains__(self, word):
        """
        check if a node exists in the trie
        """
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                return False
            current_node = current_node[letter]
        return '*' in current_node

    def __str__(self):
        """
        string representation of the trie data structure
        """
        return pprint.pformat(self.root, indent=1, compact=True)


def trie_test():
    """
    Simple checks if words belong to tries
    """
    print("Dict Trie:Test")
    trie = DictTrie()
    trie.add("Hi")
    trie.add("Hit")
    trie.add("Hitler")
    trie.add("Yes")
    trie.add("Yes'nt")

    print("Hi" in trie)
    print("Hit" in trie)
    print("No" in trie)
    print("North" in trie)
    print("Yes" in trie)

    print("Node Trie:Test")
    node_trie = NodeTrie()
    node_trie.add("Hi")
    node_trie.add("Hit")
    node_trie.add("Hitler")
    node_trie.add("Yes")
    node_trie.add("Yes'nt")

    print(node_trie.has_word("Hi"))
    print(node_trie.has_word("Hit"))
    print(node_trie.has_word("No"))
    print(node_trie.has_word("North"))
    print(node_trie.has_word("Yes"))

    print(node_trie)


if __name__ == "__main__":
    trie_test()
