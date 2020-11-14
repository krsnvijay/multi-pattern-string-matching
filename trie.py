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


trie_test()
