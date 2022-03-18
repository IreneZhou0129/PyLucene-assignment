import os, re
import numpy as np

PYLUCENE_PATH='/Users/xiaoxinzhou/Documents/2022_classes/PyLucene-assignment'
all_eval_res = f'{PYLUCENE_PATH}/a1/all_eval_res'

def process_eval_res():
    '''
    remove extra lines from result text file, only keep
    MAP, GM_MAP, P@5, P@10, P@100, P@1000
    '''
    keep_pattern = re.compile(r'map|gm_map|P_5|P_10|P_100|P_1000.*')

    for filename in os.listdir(all_eval_res):
        
        filepath = f'{all_eval_res}/{filename}'
        with open(filepath, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for l in lines:
                if keep_pattern.match(l):
                    f.write(l)
            f.truncate()

# process_eval_res()            


def convert_res_to_np():
    '''
    iterate through the processed text files obtained from the above function.
    save all data into a 4x18 numpy array, which will be fed into a Pandas dataframe. 
                                                        1-50(a)                                                     51-100(b)   101-150(c)                                          
                                [col1]map [col2]gm_map [col3]p@5 [col4]p@10 [col5]p@100 [col6]p@500 [col7]p@1000    [col8-14]   [col16-22]
    [row1]nostop_noporter (1-i)
    [row2]                (1-ii)
    [row3]                (1-iii)
    [row4]nostop_porter   (3-i)
    [row5]                (3-ii)
    [row6]                (3-iii)
    [row7]stop_noporter   (2-i)
    [row8]                (2-ii)
    [row9]                (2-iii)
    [row10]stop_porter    (4-i)
    [row11]               (4-ii)
    [row12]               (4-iii)
    '''
    col = 0
    res = np.zeros((12, 21))
    
    # filename determines the row number
    row_nums = {
        '1-i':0, '1-ii':1, '1-iii':2,
        '3-i':3, '3-ii':4, '3-iii':5,
        '2-i':6, '2-ii':7, '2-iii':8,
        '4-i':9, '4-ii':10, '4-iii':11,
    }

    # middle letter determines the column area
    col_groups = {
        'a': 0,
        'b': 7,
        'c': 14
    }

    # filename: '1-a-i_eval.txt'
    for filename in os.listdir(all_eval_res):

        # convert '1-a-i_eval.txt' into '1-i'
        l = filename.split('_')[0].split('-')
        s = '-'.join([l[0],l[2]])
        row = row_nums[s]

        topics = col_groups[l[1]]

        filepath = f'{all_eval_res}/{filename}'
        with open(filepath, 'r+') as f:
            lines = f.readlines()

            for line in lines:
                if 'gm_map' in line:
                    col = topics+1

                elif 'map' in line:
                    col = topics

                elif 'P_500' in line:
                    col = topics+6

                elif 'P_1000' in line:
                    col = topics+5

                elif 'P_100' in line:
                    col = topics+4

                elif 'P_10' in line:
                    col = topics+3

                elif 'P_5' in line: 
                    col = topics+2

                res[row][col] = float(line.split('all\t')[-1].strip())
    print(res)
    return res

convert_res_to_np()