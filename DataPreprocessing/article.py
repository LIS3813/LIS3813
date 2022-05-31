from module.mymodule import load_pipeline, parse_date_time, execute, splite_sentence
import pandas as pd

# init
pipe = load_pipeline()
date_all = []
sentence_all = []
label_all = []

# read all data files
for index in range(0, 1000):
    # read single file
    try :
        datafile = pd.read_csv(f'./DATA/article/df{index}_article.csv')
    except:
        print(f'not exist file df{index}_article.csv')
        continue
    # read single row    
    for _, row in datafile.iterrows():
        date_time = parse_date_time(row["date"])
        
        # get title data
        if row["title"] != '0':
            date_all.append(date_time)
            sentence_all.append(row["title"])
            label_all.append(execute(pipe, row["title"]))

        # get article sentence labels 
        for article in splite_sentence(row["article"]):
            if (article == '') or (article == '0'):
                continue
            date_all.append(date_time)
            sentence_all.append(article)
            label_all.append(execute(pipe, article))
    print(f'finish {index}')

#convert dataframe to csv
result = pd.DataFrame(
    zip( date_all, sentence_all, label_all), 
    columns = ['date', 'sentence', 'label'])
result.to_csv("df_article.csv")