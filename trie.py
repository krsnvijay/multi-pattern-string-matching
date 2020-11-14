import pprint


class Trie:
    def __init__(self):
        self.root = {'*': '*'}

    def add(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                current_node[letter] = {}
            current_node = current_node[letter]
        current_node['*'] = '*'

    def contains(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                return False
            current_node = current_node[letter]
        return '*' in current_node

    def __str__(self):
        return pprint.pformat(self.root, indent=1, compact=True)


def trie_test():
    trie = Trie()
    trie.add("Hi")
    trie.add("Hit")
    trie.add("Hitler")
    trie.add("Yes")
    trie.add("Yes'nt")

    print(trie.contains("Hi"))
    print(trie.contains("Hit"))
    print(trie.contains("No"))
    print(trie.contains("North"))
    print(trie.contains("Yes"))


if __name__ == "__main__":
    trie_test()
