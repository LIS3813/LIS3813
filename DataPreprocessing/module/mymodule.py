from numpy import NaN
from transformers import TextClassificationPipeline, BertForSequenceClassification, TrainingArguments, Trainer, AutoTokenizer
import datetime as dt

def parse_date_time( date_str : str):
    result : dt.datetime
    try:
        result = dt.datetime.strptime(date_str, '%y/%m/%d %H:%M')
    except:
        result = dt.datetime.strptime(f'22/{date_str}', '%y/%m/%d %H:%M')
    return result

def load_pipeline():
    model_path = './model_output'
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    pipe = TextClassificationPipeline(
        model = model,
        tokenizer = tokenizer,
        device=-1,
        return_all_scores=True,
        function_to_apply='sigmoid'
    )
    return pipe

def execute(pipe : TextClassificationPipeline, data_str : str):  
    max = 0
    label :str
    try :
        for result in pipe(data_str)[0]:
            if max <= result["score"]:
                max = result["score"]
                label = result["label"]
        return label
    except :
        return "clean"

# def splite_word(okt :Okt, word : str):
#     return okt.phrases(word)

def splite_sentence(data : str):
    return data.split('\n')
