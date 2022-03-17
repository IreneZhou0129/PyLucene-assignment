#!/bin/bash

# variables
A1_DATA_PATH='/Users/xiaoxinzhou/Documents/2022_classes/a1-data'
PYLUCENE_PATH='/Users/xiaoxinzhou/Documents/2022_classes/PyLucene-assignment'

SAMPLES=$PYLUCENE_PATH/samples

################################################
# Indexing
# 1. not use stop words
# 2. use stop words
################################################
# 1. [done] Default 
python $SAMPLES/IndexFiles.py $A1_DATA_PATH/AP "IndexFiles.index"

# 2. [done] Using stop words
python $SAMPLES/IndexFiles.py $A1_DATA_PATH/AP "IndexFiles_stop_words.index" "-stop"


################################################
# Searching

# a. 1-50
# b. 51-100
# c. 101-150

# i. VSM
# ii. BM25
# iii. Dirichlet
################################################

# 1-a-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '1-50' 'IndexFiles.index'

# 1-b-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '51-100' 'IndexFiles.index'

# 1-c-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '101-150' 'IndexFiles.index'

# 2-a-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '1-50' 'IndexFiles_stop_words.index' '-stop'

# 2-b-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '51-100' 'IndexFiles_stop_words.index' '-stop'

# 2-c-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '101-150' 'IndexFiles_stop_words.index' '-stop'

#  ii. BM25
# 1-a-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '1-50' 'IndexFiles.index'

# 1-b-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '51-100' 'IndexFiles.index'

# 1-c-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '101-150' 'IndexFiles.index'

# 2-a-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '1-50' 'IndexFiles_stop_words.index' '-stop'

# 2-b-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '51-100' 'IndexFiles_stop_words.index' '-stop'

# 2-c-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '101-150' 'IndexFiles_stop_words.index' '-stop'

# iii. Dirichlet
# 1-a-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '1-50' 'IndexFiles.index'

# 1-b-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '51-100' 'IndexFiles.index'

# 1-c-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '101-150' 'IndexFiles.index'

# 2-a-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '1-50' 'IndexFiles_stop_words.index' '-stop'

# 2-b-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '51-100' 'IndexFiles_stop_words.index' '-stop'

# # 2-c-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '101-150' 'IndexFiles_stop_words.index' '-stop'

################################################
# Evaluating
################################################
# i. VSM
# 1-a-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/1-a-i.txt >> $PYLUCENE_PATH/a1/eval_res/1-a-i_eval.txt

# 1-b-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/1-b-i.txt >> $PYLUCENE_PATH/a1/eval_res/1-b-i_eval.txt

# 1-c-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/1-c-i.txt >> $PYLUCENE_PATH/a1/eval_res/1-c-i_eval.txt

# 2-a-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/2-a-i.txt >> $PYLUCENE_PATH/a1/eval_res/2-a-i_eval.txt

# 2-b-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/2-b-i.txt >> $PYLUCENE_PATH/a1/eval_res/2-b-i_eval.txt

# 2-c-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/2-c-i.txt >> $PYLUCENE_PATH/a1/eval_res/2-c-i_eval.txt

# ii. BM25 
# 1-a-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/1-a-ii.txt >> $PYLUCENE_PATH/a1/eval_res/1-a-ii_eval.txt

# 1-b-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/1-b-ii.txt >> $PYLUCENE_PATH/a1/eval_res/1-b-ii_eval.txt

# 1-c-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/1-c-ii.txt >> $PYLUCENE_PATH/a1/eval_res/1-c-ii_eval.txt

# 2-a-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/2-a-ii.txt >> $PYLUCENE_PATH/a1/eval_res/2-a-ii_eval.txt

# 2-b-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/2-b-ii.txt >> $PYLUCENE_PATH/a1/eval_res/2-b-ii_eval.txt

# 2-c-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/2-c-ii.txt >> $PYLUCENE_PATH/a1/eval_res/2-c-ii_eval.txt

# iii. Dirichlet
# 1-a-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/1-a-iii.txt >> $PYLUCENE_PATH/a1/eval_res/1-a-iii_eval.txt

# 1-b-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/1-b-iii.txt >> $PYLUCENE_PATH/a1/eval_res/1-b-iii_eval.txt

# 1-c-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/1-c-iii.txt >> $PYLUCENE_PATH/a1/eval_res/1-c-iii_eval.txt

# 2-a-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/2-a-iii.txt >> $PYLUCENE_PATH/a1/eval_res/2-a-iii_eval.txt

# 2-b-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/2-b-iii.txt >> $PYLUCENE_PATH/a1/eval_res/2-b-iii_eval.txt

# 2-c-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/2-c-iii.txt >> $PYLUCENE_PATH/a1/eval_res/2-c-iii_eval.txt