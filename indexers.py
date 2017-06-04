# Indexing engines


class HashTableIndexer:

    """
    This one is only good for exact matches
    """

    def __init__(self):
        self.HashMap = dict()

    def index(self, key, index):

        if key not in self.HashMap:
            self.HashMap[key] = list()

        # Add Index object to bucket
        self.HashMap[key].append(index)

    def search(self, key):

        # Because we are looking for exact matches we just check if the key exists in our dictionary
        if key in self.HashMap:
            return self.HashMap[key]

        return list()


class TreeIndexer:

    """
    This one is slightly better one memory and is great for partial matching.
    """

    class Node:

        def __init__(self):
            self.storage = dict()
            self.indexes = list()

        def add(self, word, index):

            if word[0] not in self.storage:
                self.storage[word[0]] = self.__class__()

            self.indexes.append(index)

            if len(word) > 1:
                return self.child(word[0]).add(word[1:], index)
            else:
                return True

        def has(self, letter):
            return letter in self.storage

        def child(self, letter):
            return self.storage[letter]

        def fetch_indexes(self):
            return self.indexes

    STYLE_EXACT = 1
    STYLE_PARTIAL = 0

    def __init__(self):
        self.head = self.Node()

    def search(self, word, style=0, minimum=3):
        p = self.head
        l = word[0]
        o = word
        steps = 0

        while p.has(l):
            p = p.child(l)
            word = word[1:]
            steps += 1

            if len(word) > 1:
                l = word[0]
            else:
                break

        if style == self.STYLE_PARTIAL and steps >= minimum:
                return p.fetch_indexes()

        if style == self.STYLE_EXACT and steps == (len(o) - 1):
                return p.fetch_indexes()

        return list()

    def index(self, word, index):
        self.head.add(word, index)
