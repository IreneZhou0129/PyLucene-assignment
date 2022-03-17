#!/bin/bash

# variables
A1_DATA_PATH='/Users/xiaoxinzhou/Documents/2022_classes/a1-data'
PYLUCENE_PATH='/Users/xiaoxinzhou/Documents/2022_classes/PyLucene-assignment'

SAMPLES=$PYLUCENE_PATH/samples

################################################
# Indexing
# 1. not use stop words
# 2. use stop words
# 3. porter + not use stop words
# 4. porter + use stop words
################################################
# 3. [done] porter + not use stop words 
python $SAMPLES/IndexFiles.py $A1_DATA_PATH/AP "IndexFiles_porter_no_stop.index" "-porter"

# 4. [done] porter + use stop words
python $SAMPLES/IndexFiles.py $A1_DATA_PATH/AP "IndexFiles_porter_and_stop.index" "-stop" "-porter"


################################################
# Searching

# a. 1-50
# b. 51-100
# c. 101-150

# i. VSM
# ii. BM25
# iii. Dirichlet

# recall 
# 3. porter + not use stop words
# 4. porter + use stop words
################################################

# 3-a-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '1-50' 'IndexFiles_porter_no_stop.index' '-porter'

# 3-b-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '51-100' 'IndexFiles_porter_no_stop.index' '-porter'

# 3-c-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '101-150' 'IndexFiles_porter_no_stop.index' '-porter'

# 4-a-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '1-50' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

# 4-b-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '51-100' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

# 4-c-i [done]
python $SAMPLES/SearchFiles.py 'vsm' '101-150' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

 ii. BM25
3-a-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '1-50' 'IndexFiles_porter_no_stop.index' '-porter'

# 3-b-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '51-100' 'IndexFiles_porter_no_stop.index' '-porter'

# 3-c-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '101-150' 'IndexFiles_porter_no_stop.index' '-porter'

# 4-a-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '1-50' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

# 4-b-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '51-100' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

# 4-c-ii [done]
python $SAMPLES/SearchFiles.py 'bm25' '101-150' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

iii. Dirichlet
3-a-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '1-50' 'IndexFiles_porter_no_stop.index' '-porter'

# 3-b-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '51-100' 'IndexFiles_porter_no_stop.index' '-porter'

# 3-c-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '101-150' 'IndexFiles_porter_no_stop.index' '-porter'

# 4-a-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '1-50' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

# 4-b-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '51-100' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

# # 4-c-iii [done]
python $SAMPLES/SearchFiles.py 'dirichlet' '101-150' 'IndexFiles_porter_and_stop.index' '-porter' '-stop'

# ################################################
# # Evaluating
# ################################################
# i. VSM
# 3-a-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/3-a-i.txt >> $PYLUCENE_PATH/a1/eval_res/3-a-i_eval.txt

# 3-b-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/3-b-i.txt >> $PYLUCENE_PATH/a1/eval_res/3-b-i_eval.txt

# 3-c-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/3-c-i.txt >> $PYLUCENE_PATH/a1/eval_res/3-c-i_eval.txt

# 4-a-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/4-a-i.txt >> $PYLUCENE_PATH/a1/eval_res/4-a-i_eval.txt

# 4-b-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/4-b-i.txt >> $PYLUCENE_PATH/a1/eval_res/4-b-i_eval.txt

# 4-c-i [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/4-c-i.txt >> $PYLUCENE_PATH/a1/eval_res/4-c-i_eval.txt

# ii. BM25 
# 3-a-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/3-a-ii.txt >> $PYLUCENE_PATH/a1/eval_res/3-a-ii_eval.txt

# 3-b-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/3-b-ii.txt >> $PYLUCENE_PATH/a1/eval_res/3-b-ii_eval.txt

# 3-c-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/3-c-ii.txt >> $PYLUCENE_PATH/a1/eval_res/3-c-ii_eval.txt

# 4-a-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/4-a-ii.txt >> $PYLUCENE_PATH/a1/eval_res/4-a-ii_eval.txt

# 4-b-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/4-b-ii.txt >> $PYLUCENE_PATH/a1/eval_res/4-b-ii_eval.txt

# 4-c-ii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/4-c-ii.txt >> $PYLUCENE_PATH/a1/eval_res/4-c-ii_eval.txt

# iii. Dirichlet
# 3-a-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/3-a-iii.txt >> $PYLUCENE_PATH/a1/eval_res/3-a-iii_eval.txt

# 3-b-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/3-b-iii.txt >> $PYLUCENE_PATH/a1/eval_res/3-b-iii_eval.txt

# 3-c-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/3-c-iii.txt >> $PYLUCENE_PATH/a1/eval_res/3-c-iii_eval.txt

# 4-a-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.1-50.AP8890 $PYLUCENE_PATH/a1/4-a-iii.txt >> $PYLUCENE_PATH/a1/eval_res/4-a-iii_eval.txt

# 4-b-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.51-100.AP8890 $PYLUCENE_PATH/a1/4-b-iii.txt >> $PYLUCENE_PATH/a1/eval_res/4-b-iii_eval.txt

# 4-c-iii [done]
trec_eval-9.0.7/trec_eval $A1_DATA_PATH/qrels.101-150.AP8890 $PYLUCENE_PATH/a1/4-c-iii.txt >> $PYLUCENE_PATH/a1/eval_res/4-c-iii_eval.txt