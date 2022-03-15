#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
from datetime import datetime
import gzip

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
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

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(Paths.get(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print ('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print ('done')

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:

                try:
                    # filename=='AP881210.gz', open it 
                    path = os.path.join(root, filename)

                    f=gzip.open(path,'rb')

                    # TODO Need to extract document_no:
                    # e.g., <DOCNO> AP881210-0148
                    bytes_content=f.read()
                    print ("adding", filename)

                    # and convert bytes to strings
                    contents = bytes_content.decode("utf-8") 

                    f.close()
                    # breakpoint()
                    doc = Document()
                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", root, t1))
                    doc.add(Field("docno", docno, t1))

                    if len(contents) > 0:
                        doc.add(Field("contents", contents, t2))
                    else:
                        print ("warning: no content in %s" % filename)
                    writer.addDocument(doc)
                except Exception as e:
                    print ("Failed in indexDocs:", e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print (IndexFiles.__doc__)
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer())
        end = datetime.now()
        print (end - start)
    except Exception as e:
        print ("Failed: ", e)
        raise e
