from database import Cluster
from indexers import TreeIndexer, HashTableIndexer
import os
import time

storage = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/storage')
data = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/small_sample.csv')
t_secs = lambda: int(round(time.time()))

print('Starting up...')

start_up_t = t_secs()
c = Cluster(storage, data, 'last_name', TreeIndexer())

print('Started up in ' + str(t_secs() - start_up_t) + ' seconds')
print('Loaded ' + str(c.total_records) + ' records')

while True:
    key = input('Enter search term:')
    s_time = t_secs()
    c.search_print(key)
    e_time = t_secs() - s_time

    print('Searched through ' + str(c.total_records) + ' records in ' + str(e_time) + '  seconds')
    break
