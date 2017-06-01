#
#  A single index search script
#  Carlos Granados <granados.carlos91@gmail.com>
#


from collections import namedtuple
from prettytable import PrettyTable
from multiprocessing import Process
import csv
import re
import os
import shutil

Index = namedtuple('Index', ['node', 'line'])


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped()


class Cluster:

    def __init__(self, storage_location, load_file, index_col):

        self.MAX_NODE_SIZE = 1000
        self.MAX_PROCESS_POOL_SIZE = 10
        self.storage = self.validate_storage(storage_location)
        self.file_location = self.validate_path(load_file)
        self.HashMap = dict()
        self.index_col = index_col
        self.index_pos = None
        self.column_names = None
        self.total_records = 0

        self.start_up()

    def start_up(self):

        with open(self.file_location) as file:
            reader = csv.reader(file, delimiter=',')
            node_counter = 0
            line = 0
            node = self.init_node(node_counter)
            self.column_names = next(reader)

            try:
                self.index_pos = self.column_names.index(self.index_col)
            except:
                raise "Invalid index, column with name " + self.index_col + " does not exist in this data set"

            for row in reader:

                if line == self.MAX_NODE_SIZE:
                    node.close()
                    node_counter += 1
                    line = 0
                    node = self.init_node(node_counter)

                key = self.norm(row[self.index_pos])
                self.track(key, node_counter, line)
                node.write(','.join(row) + '\n')

                self.total_records += 1
                line += 1

    def validate_path(self, path):

        if not os.path.isfile(path):
            raise "CSV is invalid (File does not exist or is not a csv file): " + path

        return path

    def track(self, key, node, line):
        i = Index(node=node, line=line)

        if key not in self.HashMap:
            self.HashMap[key] = list()

        self.HashMap[key].append(i)

    def norm(self, key):
        return re.sub('[^a-zA-Z0-9]', '', key).lower()

    def init_node(self, number):
        return open(self.make_node_file_name(number), '+a')

    def read_node(self, number):
        return open(self.make_node_file_name(number), 'r')

    def make_node_file_name(self, number):
        return self.storage + '/' + str(number) + '.db'

    def search(self, key):
        key = self.norm(key)

        if key in self.HashMap:

            indexes = self.HashMap[key]

            for i in indexes:
                yield self.fetch(i)

    def validate_storage(self, storage):

        if os.path.exists(storage):
            shutil.rmtree(storage)

        os.makedirs(storage)

        return storage

    def fetch(self, i):
        p = self.read_node(i.node)
        line = 0

        for row in p:
            if line == i.line:
                return row

            line += 1

    def search_print(self, key):
        table = PrettyTable(self.column_names)

        for row in self.search(key):
            table.add_row(row.split(','))

        print(table)
