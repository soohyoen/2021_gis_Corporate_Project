import pandas as pd
import numpy as np
import json
import re

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json

from konlpy.tag import Hannanum

model = load_model('./ml/model.h5')
with open('./ml/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)
MAX_LEN = 35
STOP_WORDS = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', 
            '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임',
            '만', '겜', '되', '음', '면', '제', '항', '저', '및', '으로', '어',
            '등', '이나', '또는', '보', 'ㄴ', '어서', '늘', '모든', '대', '에서', '갑']

def predict_test(new_sentence):
    hannanum = Hannanum()
    new_sentence = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", " ", new_sentence)
    new_sentence = hannanum.morphs(new_sentence)
    new_sentence = [word for word in new_sentence if not word in STOP_WORDS]
    encoded = tokenizer.texts_to_sequences([new_sentence])
    pad_new = pad_sequences(encoded, maxlen=MAX_LEN, padding='post')
    score = model.predict(pad_new)

    return np.argmax(score[0])


def analysis(articles):
    result = []
    model_predict = []
    for text in articles:
        predict = predict_test(text)
        model_predict.append(predict)

    model_predict.sort()
    return set(model_predict)