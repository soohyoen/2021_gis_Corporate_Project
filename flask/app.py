from flask import Flask, request, render_template, jsonify
import asyncio
import os
import json

from src.ocr import ocr_task, merge, split_article
from src.model import analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/analysis/contract", methods=["POST"])
def contract_analysis():
    print('/api/analysis/contract 호출')

    upload = request.files.getlist("file[]")

    # 입력으로 들어온 파일들에 대해서 비동기적으로 OCR 과정 수행
    splited_contract_doc = asyncio.run(ocr_task(upload))
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # splited_contract_doc = loop.run_until_complete(ocr_task(upload))
    # loop.close()

    ocr_json = []
    for filename in os.listdir('./public/tmp'):
        with open(f'./public/tmp/{filename}', 'r', encoding="UTF-8") as f:
            ocr_json.append(json.load(f))
    # print(ocr_json)
    
    # 로드 json 결과물 (Clova OCR 에서 정상적으로 결과가 들어왔다 치고)
    full_contract_doc = merge(ocr_json)
    articles = split_article(full_contract_doc)
    model_predict = analysis(articles)

    not_include_list = list({i for i in range(1,21)} - model_predict)

    print(model_predict)
    print(not_include_list)

    return jsonify({"notIncludeArticle": not_include_list})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
