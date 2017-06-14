# Indexing engines
import inspect


class IndexingEngine:

    def index(self, key, index):
        self._err(inspect.stack()[0][3])

    def search(self, key):
        self._err(inspect.stack()[0][3])

    def _err(self, f):
        raise Exception("You must implement " + f + " in your indexer class.")


class HashTableIndexer(IndexingEngine):

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


class TreeIndexer(IndexingEngine):

    """
    Good for partial matching
    """

    class Node:

        def __init__(self):
            self.storage = dict()
            self.indexes = list()
            self.ending_indices = list()

        def add(self, word, index):

            # Check if we're already tracking this letter at this level
            if word[0] not in self.storage:
                self.storage[word[0]] = self.__class__()

            # Add index to list in this node
            self.indexes.append(index)

            # If the word is still not done pass remaining string into the child node
            # for the next letter
            if len(word) > 1:
                return self.child(word[0]).add(word[1:], index)
            else:
                # Keep track of indexes for words that end here
                self.ending_indices.append(len(self.indexes) - 1)
                return True

        def has(self, letter):
            return letter in self.storage

        def child(self, letter):
            return self.storage[letter]

        def fetch_indexes(self, continuous=True):
            if continuous is True:
                return self.indexes

            # This is so we can do exact matching
            return [self.indexes[i] for i in self.ending_indices]

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

        if style == self.STYLE_PARTIAL and steps >= (minimum - 1):
                return p.fetch_indexes()

        if style == self.STYLE_EXACT and steps == (len(o) - 1):
                return p.fetch_indexes(continuous=False)

        return list()

    def index(self, word, index):
        self.head.add(word, index)
