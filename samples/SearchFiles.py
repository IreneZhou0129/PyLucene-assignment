#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"
PATH_PREFIX = "/Users/xiaoxinzhou/Documents/2022_classes"

import sys, os, lucene, re, time
from datetime import datetime
from subprocess import Popen, PIPE

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

from org.apache.lucene.search.similarities import BM25Similarity,\
                                                ClassicSimilarity,\
                                                LMDirichletSimilarity

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

def run(searcher, analyzer, query_paths, topics, model):
    """

    :param query_paths: A list of paths. 
    :param model: default value is 'vsm'.
    """

    print(f"Starting to run {model}.\n")
    start = time.time()

    # write to a text file
    result_filename = f'a1/{model}_{topics}_result.txt'
    f = open(result_filename, 'a')

    # record model statistics
    model_stats = open(f'a1/model_stats.txt', 'a')

    # select topics
    topics_paths = {
        "1-50": query_paths[0],
        "51-100": query_paths[1],
        "101-150": query_paths[2],
    }

    query_file = topics_paths[topics]
    queries = get_queries(query_file) # a list of queries

    # initialize query ID
    q_id = 1

    for q in queries:

        # handle special characters in query
        q = QueryParser("contents", analyzer).escape(q)

        # https://lucene.apache.org/core/7_3_0/queryparser/org/apache/lucene/queryparser/classic/QueryParserBase.html
        query = QueryParser("contents", analyzer).parse(q)

        # https://lucene.apache.org/core/9_0_0/core/org/apache/lucene/search/IndexSearcher.html#search(org.apache.lucene.search.Query,int)
        scoreDocs = searcher.search(query, 1000).scoreDocs

        print( "%s top matching documents." % len(scoreDocs))

        rank = 1
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)

            # trec_results need to have format
            # Lines of results_file are of the form
            # 030  Q0  ZF08-175-870  0   4238   prise1
            # qid iter   docno      rank  sim   run_id
            docno = doc.get('docno').strip()

            log = f"{q_id}  0  {docno}   {rank}  {scoreDoc.score}    run_id"
            # print(log)

            rank += 1
            
            # write to result text file
            f.write(log)
            f.write('\n')
        
        q_id += 1

    end = time.time()
    print(f"Done model {model}. \nRunning process takes {end-start}")
    
    model_stats.write(f'{datetime.now()}  Model: {model}       Topics:{topics}        Running time: {end-start} seconds.')
    f.close()
    model_stats.close()
        

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print( 'lucene: '+lucene.VERSION)
    model=None
    # model = input("vsm, bm25 or dirichlet: ")
    # topics = input("1-50, 51-100 or 101-150: ")

    # '/Users/.../PyLucene-assignment/samples'
    ########################
    # select topics file
    ########################
    query_paths = [f'{PATH_PREFIX}/a1-data/topics.1-50.txt',
                   f'{PATH_PREFIX}/a1-data/topics.51-100.txt',
                   f'{PATH_PREFIX}/a1-data/topics.101-150.txt']

    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    
    searcher = IndexSearcher(DirectoryReader.open(directory))

    ########################
    # set retrieval model
    ########################
    # tf-idf is default scheme: https://lists.archive.carbon60.com/lucene/java-user/201216
    if model == 'bm25':
        searcher.setSimilarity(BM25Similarity())
    elif model == 'dirichlet':
        searcher.setSimilarity(LMDirichletSimilarity())
    else:
        searcher.setSimilarity(ClassicSimilarity())

    analyzer = StandardAnalyzer()
    
    model = 'vsm'
    topics = '1-50'
    run(searcher, analyzer, query_paths, topics, model)
    del searcher
