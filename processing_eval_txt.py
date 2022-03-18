import os, re

PYLUCENE_PATH='/Users/xiaoxinzhou/Documents/2022_classes/PyLucene-assignment'

def process_eval_res():
    '''
    remove extra lines from result text file, only keep
    MAP, GM_MAP, P@5, P@10, P@100, P@1000
    '''
    all_eval_res = f'{PYLUCENE_PATH}/a1/all_eval_res'

    keep_pattern = re.compile(r'map|gm_map|P_5|P_10|P_100|P_1000.*')

    for filename in os.listdir(all_eval_res):
        try:
            filepath = f'{all_eval_res}/{filename}'
            with open(filepath, 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                for l in lines:
                    if keep_pattern.match(l):
                        f.write(l)
                f.truncate()
        except FileNotFoundError:
            print(f"File {filename} is not found.")
            continue

process_eval_res()            