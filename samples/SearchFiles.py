#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"
PATH_PREFIX = "/Users/xiaoxinzhou/Documents/2022_classes"

import sys, os, lucene, re, time

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

# helper functions
def get_queries(text_file):
    """
    Read a text file, extract text(query) under tag <title>, and put all topics into a list.
    
    :param text_file: Notice that it has to be a full path. E.g., '../../a1-data/topics.1-50.txt'
    
    :return topics_list: A list of strings. 
    """

    queries = []

    # Read text line by line
    with open(text_file) as f:
        lines = f.readlines()
        
    for line in lines:    
        m=re.compile(r"<title>\sTopic:\s(?P<q>.*)")
        matched = m.match(line)
        if matched:
            query = matched.group("q")
            queries.append(query)    
    
    return queries

def run(searcher, analyzer, query_paths):
    """

    :param query_paths: A list of paths. 
    """

    print("Starting to run\n")
    start = time.time()

    # loop over query paths
    for query_file in query_paths:
        queries = get_queries(query_file) # a list of queries

        for q in queries:

            # handle special characters in query
            q = QueryParser("contents", analyzer).escape(q)

            # https://lucene.apache.org/core/7_3_0/queryparser/org/apache/lucene/queryparser/classic/QueryParserBase.html
            query = QueryParser("contents", analyzer).parse(q)

            # https://lucene.apache.org/core/9_0_0/core/org/apache/lucene/search/IndexSearcher.html#search(org.apache.lucene.search.Query,int)
            scoreDocs = searcher.search(query,3).scoreDocs

            print( "%s top matching documents." % len(scoreDocs))

            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                # print(f"path: {doc.get('path')} name: {doc.get('name')} score: {scoreDoc.score}")
                print(f"query: {q}; doc_name: {doc.get('name')} doc_score: {scoreDoc.score}")
    
    end = time.time()
    print(f"Running process takes {end-start}")

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print( 'lucene: '+lucene.VERSION)

    # '/Users/.../PyLucene-assignment/samples'
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()

    query_paths = [f'{PATH_PREFIX}/a1-data/topics.1-50.txt',
                   f'{PATH_PREFIX}/a1-data/topics.51-100.txt',
                   f'{PATH_PREFIX}/a1-data/topics.101-150.txt']

    run(searcher, analyzer, query_paths)
    del searcher
