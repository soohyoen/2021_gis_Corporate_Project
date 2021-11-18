from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import asyncio
import os
import json

from src.ocr import ocr_task, merge, split_article
from src.model import analysis

app = Flask(__name__)
CORS(app, resource={
    '/api/*': {'origin': '*'}
})

@app.route("/api/analysis/contract", methods=["POST"])
def contract_analysis():
    print('/api/analysis/contract 호출')

    upload = request.files.getlist("file[]")

    # 입력으로 들어온 파일들에 대해서 OCR 과정 수행
    # 테스트 중에는 동작하지 않도록 주석처리
    ocr_json = asyncio.run(ocr_task(upload))

    # ocr_json = []
    # for filename in os.listdir('./public/tmp'):
    #     with open(f'./public/tmp/{filename}', 'r', encoding="UTF-8") as f:
    #         ocr_json.append(json.load(f))
    
    # 로드 json 결과물 (Clova OCR 에서 정상적으로 결과가 들어왔다 치고)
    full_contract_doc = merge(ocr_json)
    if not full_contract_doc:
        return jsonify({'status': 'fail'})

    articles = split_article(full_contract_doc)
    model_predict = analysis(articles)

    not_include_list = list({i for i in range(1,21)} - model_predict)

    return jsonify({"status": 'succuess', "notIncludeArticle": not_include_list})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
