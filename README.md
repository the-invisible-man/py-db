# Search Store

A simple script for loading a csv file and searching through it. It  takes an approach similar to that of popular document search engines, the data is broken up into smaller documents (nodes) and the indexes are tracked by the node identifier and the line number. The engine comes with a sample data file with 1.2 million records.

*Alternate Technique:* (Not implemented in this repo) If we didn't want to have the in memory indexes of all the data we would have to sort the data by the last_name column, then split it, then write it. For searching we could then use binary search concurrently on every node, then take note of the node and line number and use the in memory indexing strategy for caching the results.

## Requirements
Python 3.0 ^

## Instructions
This project requires prettytable for displaying the data in a nice format.
```
pip install -r requirements.txt
```

Run the search:
```
python search.py
```

### Last Names in the Data:
Due to limitations in most free csv data generators, the data repeats after 1000 records. Here are some last names that will return results, each should return a large number of results since the data repeats.

* Barstowk
* Tiner
* Odger
* O'Scandall
* Lanfranchi

## Benchmark

By default the database has a maximum node size of 1000, the larger the node size, the shorter the startup time but the longer the search time. With a 1000 max document size the startup will be around 6-9 seconds on a modern CPU and the search will take around 1 second.

## Indexing

This implementation comes with two indexers that are used for different purposes, these indexers are the HashTableIndexer and the TreeIndexer. The hash table indexer allows only for exact matches on the lastnames (case insensitive), while the TreeIndexer allows for partial matching (case insensitive).

### HashTableIndexer
On startup the engine loads the csv file with the mock data. Using the last_name column as a key, the engine uses a dictionary to track all unique occurrences of a last_name. In order to account for lowercase and special symbols, we remove any non-alphanumeric characters and we lowercase the last_name. The key maps to a list of `Index` types, this type is a namedtuple and there is one for each entry. The tuple `Index` contains only two fields, a `node` and a `line`. Using this tuple we know in which node to find the data and in what line.

![alt text](https://raw.githubusercontent.com/the-invisible-man/python-search/master/assets/indexing.png "Indexing")

### TreeIndexer
The tree indexer implements are similar concept to the HashTableIndexer in that it keeps track of the node and line number where the data can be found, but the data structure is much more different. As of this moment the py-db engine is able to do partial matching on the start of the string. This allows us to add the `%` operator to command the search to do a partial search. In practice this would allows us to store the lastnames "John" and "Johnson", search with the string `john%` and receive both lastnames. This is achieved with the help of a [Trie](https://en.wikipedia.org/wiki/Trie) data structure, however it is important to note of the increase in space complexity when dealing with tree sturctures. This indexer has been benchedmarked as peaking to a little over 250mb of memory usage for over a million records. The following image illustrates how the TreeIndexer would store the strings `john` and `johnson` in memory. 

![alt text](https://raw.githubusercontent.com/the-invisible-man/py-db/master/assets/trie.png "Trie")

## Searching

Once all the data has been indexed we can type our first search query. The search will accept an alphanumeric string, all other characters will be ignored and the string will be lower cased. Using this string we'll check the dictionary we use for tracking our indexes and check if the key exists. If the key does in fact exist then we can fetch the value which will be a list of `Index` types. These objects will tell us exactly where to find our record.

*Other Notes:* The costlier part in the search in terms of time is the disk IO to fetch each individual file. One way to speed this part up is using Python's `multiprocessing` library to concurrently fetch the data from each node. Likewise we can do this with the indexing to dramatically speed it up.

*Alternate Technique:* If we didn't want to have the in memory indexes we would have to sort the data by the last_name column, then split it, then write it. For searching we could then use binary search concurrently on every node.

![alt text](https://raw.githubusercontent.com/the-invisible-man/python-search/master/assets/searching.png "Searching")
