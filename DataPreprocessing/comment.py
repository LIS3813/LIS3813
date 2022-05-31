from module.mymodule import load_pipeline, parse_date_time, execute, splite_sentence
import pandas as pd
import re

# init
pipe = load_pipeline()
date_all = []
sentence_all = []
label_all = []

# read all data files
for index in range(0, 1000):
    # read single file
    try:
        datafile = pd.read_csv(f'./DATA/comment/df{index}_comment.csv')
    except:
        print(f'not exist file df{index}_comment.csv')
        continue

    # read single row
    for _, row in datafile.iterrows():        
        # replace comment 
        try:
            regexp = '익명[0-9]?[0-9]?\n?|공감\n?|쪽지\n?|신고\n?|없음\n?|대댓글\n?|(글쓴이)\n?|(삭제)\n?'
            row["comment"] = re.sub(regexp,"", row["comment"])            
        except:
            # nan comment
            continue

        # get comment sentence labels
        comments = []
        for sentence in splite_sentence(row["comment"]):
            sentence = re.sub('^[0-9][0-9]?\n?$|()\n?|[0-9][0-9]?분 전|된 댓글입니다.',"", sentence)
            if (sentence == '') or (sentence == '0') or (sentence == '/ :')or (sentence == '()'):
                continue
            try:
                # date
                date_time = parse_date_time(sentence)                                
                for c in comments:
                    if (c == '') or (c == '0'):
                        continue
                    date_all.append(date_time)
                    sentence_all.append(c)
                    label_all.append(execute(pipe, c))   
                comments = []             
            except:
                # comment
                comments.append(sentence)
    print(f'finish {index}')

# convert dataframe to csv
result = pd.DataFrame(
    zip( date_all,  sentence_all, label_all), 
    columns = ['date', 'sentence', 'label'])
result.to_csv("df_comment.csv")