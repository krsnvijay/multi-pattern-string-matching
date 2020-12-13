import pprint


class NodeTrie:

    def __init__(self, letter=None, parent=None, depth=0):
        self.letter = letter
        self.size = 0
        self.depth = depth
        self.parent = parent
        self.children = {}
        self.word = None
        self.failure_link = None
        self.CWsuffix_link = None
        self.CWoutput_link = None
        self.min_difference_s1 = -1
        self.min_difference_s2 = -1
        self.min_depth = None
        self.char_lookup_table = {}
        self.dictionary_link = None

    def add(self, word):
        current_node = self
        current_depth = self.depth + 1
        for letter in word:
            if letter not in current_node.children:
                next_node = NodeTrie(letter, current_node, current_depth)
                current_node.children[letter] = next_node
            else:
                next_node = current_node.children[letter]
            current_node = next_node
            current_depth += 1

        if current_node.word is not None:
            return

        current_node.word = word
        self.size += 1

    def has_word(self, word):
        current_node = self
        word = word.lower()
        for letter in word:
            if letter not in current_node.children:
                return False
            current_node = current_node.children[letter]
        return True

    def is_root(self):
        return self.letter is None

    def __contains__(self, letter):
        return letter in self.children

    def __str__(self):
        return pprint.pformat(self.children, indent=1, compact=True)

    def __repr__(self):
        return pprint.pformat(self.children, indent=1, compact=True)

    def __len__(self):
        return self.size

    def get_failure_link(self):
        suffix_matcher = self.parent.failure_link
        # get longest matching suffix
        while (not suffix_matcher.is_root()) and (self.letter not in suffix_matcher):
            suffix_matcher = suffix_matcher.failure_link

        if self.letter in suffix_matcher:
            return suffix_matcher.children[self.letter]
        else:
            if not suffix_matcher.is_root():
                print("incorrect failure links creation")
            return suffix_matcher


class DictTrie:
    def __init__(self):
        self.root = {'*': '*'}

    def add(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                current_node[letter] = {}
            current_node = current_node[letter]
        current_node['*'] = '*'

    def __contains__(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                return False
            current_node = current_node[letter]
        return '*' in current_node

    def __str__(self):
        return pprint.pformat(self.root, indent=1, compact=True)


def trie_test():
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
