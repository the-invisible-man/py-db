# Search Store

A simple script for loading a csv file and searching through it. It  takes an approach similar to that of popular document search engines, the data is broken up into smaller documents (nodes) and the indexes are tracked by the node identifier and the line number. The engine comes with a sample data file with 1.2 million records.

*Alternate Technique:* If we didn't want to have the in memory indexes we would have to sort the data by the last_name column, then split it, then write it. For searching we could then use binary search concurrently on every node.

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

By default the database has a maximum node size of 1000, the larger the node size, the shorter the startup time but the longer the search time. With a 1000 max document size the startup will be around 9 seconds and the search will take around 1 second.

## Indexing

On startup the engine loads the csv file with the mock data. Using the last_name column as a key, the engine uses a dictionary to track all unique occurrences of a last_name. In order to account for lowercase and special symbols, we remove any non-alphanumeric characters and we lowercase the last_name. The key maps to a list of `Index` types, this type is a namedtuple and there is one for each entry. The tuple `Index` contains only two fields, a `node` and a `line`. Using this tuple we know in which node to find the data and in what line.

![alt text](https://raw.githubusercontent.com/the-invisible-man/python-search/master/assets/indexing.png "Indexing")

## Searching

Once all the data has been indexed we can type our first search query. The search will accept an alphanumeric string, all other characters will be ignored and the string will be lower cased. Using this string we'll check the dictionary we use for tracking our indexes and check if the key exists. If the key does in fact exist then we can fetch the value which will be a list of `Index` types. These objects will tell us exactly where to find our record.

*Other Notes:* The costlier part in the search in terms of time is the disk IO to fetch each individual file. One way to speed this part up is using Python's `multiprocessing` library to concurrently fetch the data from each node. Likewise we can do this with the indexing to dramatically speed it up.

*Alternate Technique:* If we didn't want to have the in memory indexes we would have to sort the data by the last_name column, then split it, then write it. For searching we could then use binary search concurrently on every node.

![alt text](https://raw.githubusercontent.com/the-invisible-man/python-search/master/assets/searching.png "Searching")
