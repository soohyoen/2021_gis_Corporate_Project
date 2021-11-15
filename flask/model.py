import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Hannanum

MAX_LEN = 45
STOP_WORDS = []

def predict_test(new_sentence):
    hannanum = Hannanum()
    new_sentence = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", " ", new_sentence)
    new_sentence = hannanum.morphs(new_sentence)
    new_sentence = [word for word in new_sentence if not word in STOP_WORDS]
    encoded = tokenizer.texts_to_sequences([new_sentence])
    pad_new = pad_sequences(encoded, maxlen=MAX_LEN, padding='post')
    score = model.predict(pad_new)

    return np.argmax(score[0])


def contract_analysis(articles):
    result = []
    model_predict = []
    for text in articles:
        predict = predict_test(text)
        model_predict.append(predict)

    model_predict.sort()
    return set(model_predict)