class Parser:

    class ParserImplementationException(Exception):
        pass

    def parse(self, query):
        raise self.ParserImplementationException("You must implement parse() in your class")


class V1Engine(Parser):

    def __init__(self):
        self.query = None

    # def parse(self, query):

