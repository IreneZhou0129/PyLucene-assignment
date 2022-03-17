#!/usr/bin/env python
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
    query_num = False
    query = False
    queries = []

    # Read text line by line
    with open(text_file) as f:
        lines = f.readlines()
        
    for line in lines:    
        
        # get topic number from <num> tag
        m_q = re.compile(r"<num>\sNumber:\s(?P<q_num>.*)")
        matched_q = m_q.match(line)
        if matched_q:
            query_num = matched_q.group("q_num").strip()
            # convert '020' to 20
            query_num = int(query_num)

        m = re.compile(r"<title>\sTopic:\s(?P<q>.*)")
        matched = m.match(line)
        if matched:
            query = matched.group("q")

        # save query number and query into a tuple

        if query_num and query:
            queries.append((query_num, query)) 
            query_num = False
            query = False   
    
    return queries

def run(searcher, analyzer, query_paths, topics, model, using_stopwords):
    """

    :param query_paths: A list of paths. 
    :param model: default value is 'vsm'.
    """

    print(f"Starting to run {model}.\n")
    start = time.time()

    # write to a text file
    # file naming
    fn = {
        'topics':{
            '1-50':'a',
            '51-100':'b',
            '101-150':'c',
        },
        'model':{
            'vsm':'i',
            'bm25':'ii',
            'dirichlet':'iii'
        }
    }
    
    fn_topics = fn['topics'][topics]
    fn_model = fn['model'][model]
    no_stopword = '1' if not(using_stopwords) else '2'

    result_filename = f'PyLucene-assignment/a1/{no_stopword}-{fn_topics}-{fn_model}.txt'
    f = open(result_filename, 'a')

    # record model statistics
    model_stats = open(f'PyLucene-assignment/a1/model_stats.txt', 'a')

    # select topics
    topics_paths = {
        "1-50": query_paths[0],
        "51-100": query_paths[1],
        "101-150": query_paths[2],
    }

    query_file = topics_paths[topics]
    queries = get_queries(query_file) # a list of queries
    print(f"len(queries): {len(queries)}")

    for q_tuple in queries:

        q_num = q_tuple[0]
        q = q_tuple[1]

        # handle special characters in query
        q = QueryParser("contents", analyzer).escape(q)

        # remove duplicates
        # https://stackoverflow.com/questions/20044786/how-to-get-the-unique-results-from-lucene-index 
        # q = QueryParser("contents", analyzer).parse("central -duplicate:true")

        # https://lucene.apache.org/core/7_3_0/queryparser/org/apache/lucene/queryparser/classic/QueryParserBase.html
        query = QueryParser("contents", analyzer).parse(q)

        # https://lucene.apache.org/core/9_0_0/core/org/apache/lucene/search/IndexSearcher.html#search(org.apache.lucene.search.Query,int)
        scoreDocs = searcher.search(query, 1000).scoreDocs # a list of Document objects
        # print(f"len(scoreDocs): {len(scoreDocs)}")
        
        rank = 1
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc) # Document object

            # trec_results need to have format
            # Lines of results_file are of the form
            # 030  Q0  ZF08-175-870  0   4238   prise1
            # qid iter   docno      rank  sim   run_id

            # given qrel data format:
            # query_no, iter  doc_no        score
            # 31        0     AP880215-0238 0.02
            docno = doc.get('docno').strip()

            # log = f"{q_id}  {q_num}   {docno}   {rank}  {scoreDoc.score}      0"
            log = f"{q_num} 0 {docno} {rank} {scoreDoc.score} 0"
            rank += 1
            
            # write to result text file
            f.write(log)
            f.write('\n')
 
    f.close()

    end = time.time()
    print(f"Done model {model} with topics {topics}. using_stopwords-{using_stopwords} \nRunning process takes {end-start}")
    
    model_stats.write(f'{datetime.now()}  {no_stopword}-{fn_topics}-{fn_model}        Running time: {end-start} seconds.\n')
    model_stats.close()
        

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print( 'lucene: '+lucene.VERSION)
    
    ########################
    # user defined 
    ########################
    model = sys.argv[1]
    topics = sys.argv[2]
    INDEX_DIR = sys.argv[3]
    using_stopwords = False
    if '-stop' in sys.argv:
        using_stopwords = True

    query_paths = [f'{PATH_PREFIX}/a1-data/topics.1-50.txt',
                f'{PATH_PREFIX}/a1-data/topics.51-100.txt',
                f'{PATH_PREFIX}/a1-data/topics.101-150.txt']

    # '/Users/.../PyLucene-assignment/samples'
    ########################
    # select topics file
    ########################
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
        # TFIDFSimilarity is an abstract class. We can't instantiate it.
        # ClassicSimilarity is an implementation of it
        searcher.setSimilarity(ClassicSimilarity())
        
    analyzer = StandardAnalyzer()
    
    run(searcher, analyzer, query_paths, topics, model, using_stopwords)
    del searcher