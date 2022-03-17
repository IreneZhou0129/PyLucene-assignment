#!/usr/bin/env python

# INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime
import gzip

from PorterStemmerAnalyzer import PorterStemmerAnalyzer

from java.nio.file import Paths
from java.io import StringReader

from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis import StopFilter
from org.apache.lucene.document import Document, Field, FieldType,\
                                        StoredField, StringField, TextField
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory

"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>
        > python samples/IndexFiles.py ../a1-data/AP
    """

    def __init__(self, root, storeDir, analyzer, using_stopwords, porter_stemmer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(Paths.get(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)

        # Stop words stemming
        if using_stopwords:
            stopWords_filename = '/Users/xiaoxinzhou/Documents/2022_classes/a1-data/stop_words.txt'
            stopWords_file = open(stopWords_filename, 'r')
            stopWords = [line.replace('\n','') for line in stopWords_file.readlines()]
            stopWordsSet = StopFilter.makeStopSet(stopWords)
            analyzer = StandardAnalyzer(stopWordsSet)
        
        # Porter stemming
        if porter_stemmer:
            analyzer = PorterStemmerAnalyzer(using_stopwords)

        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)


        self.indexDocs(root, writer, using_stopwords, porter_stemmer)


        ticker = Ticker()
        print ('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print ('done')

    def indexDocs(self, root, writer, using_stopwords, porter_stemmer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        t3 = FieldType()
        t3.setStored(False)
        t3.setTokenized(True)
        t3.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:

                try:
                    # filename=='AP881210.gz', open it 
                    path = os.path.join(root, filename)

                    # read .gz file
                    f = gzip.open(path,'rb')

                    # Need to extract document_no, e.g., <DOCNO> AP881210-0148
                    bytes_content=f.read()

                    # convert bytes to strings
                    contents = bytes_content.decode("ISO-8859-1") 

                    try:
                        # each item is a doc
                        docs_list = re.split('</DOC>\n\s*<DOC>', contents)
                        doc_id_pattern = '.*\<DOCNO\>(?P<doc_id>.*)\<\/DOCNO\>.*'
                        doc_id = 0

                        for doc_item in docs_list:
                            doc_id_found = re.search(doc_id_pattern, doc_item)
                            if doc_id_found:
                                doc_id = doc_id_found.group('doc_id')
                        
                            else:
                                print(f"Unable to find doc_id in {filename}\nDoc: {doc_item}")
                                breakpoint()
                            
                            doc = Document()
                            doc.add(Field("docno", doc_id, t2))
                            doc.add(Field("contents", doc_item, t3))
                            writer.addDocument(doc)
                    except Exception as e:
                        print(f"Failed with error: {e}")
                        break

                    f.close()

                except Exception as e:
                    print (f"File {filename} failed in indexDocs:", e)
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print (IndexFiles.__doc__)
        sys.exit(1)

    # set INDEX_DIR in shell file
    INDEX_DIR = sys.argv[2]

    using_stopwords = False
    if '-stop' in sys.argv:
        using_stopwords = True

    porter_stemmer = False 
    if '-porter' in sys.argv:
        porter_stemmer = True

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], \
                    os.path.join(base_dir, INDEX_DIR),\
                    StandardAnalyzer(),\
                    using_stopwords,
                    porter_stemmer)
        end = datetime.now()
        print (end - start)
    except Exception as e:
        print ("Failed: ", e)
        raise e
