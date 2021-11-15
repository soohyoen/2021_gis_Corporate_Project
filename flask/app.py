from flask import Flask, request, render_template
import asyncio

from ocr import ocr_task, merge, split_article
from model import contract_analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/api/contract-analysis", methods=["POST"])
def contract_analysis():
    print('/api/contract-analysis 호출')

    upload = request.files.getlist("file[]")

    # 입력으로 들어온 파일들에 대해서 비동기적으로 OCR 과정 수행
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    splited_contract_doc = loop.run_until_complete(ocr_task(upload))
    loop.close()

    # 로드 json 결과물 (Clova OCR 에서 정상적으로 결과가 들어왔다 치고)
    # full_contract_doc = merge(splited_contract_doc)
    # contract_articles = split_article(full_contract_doc)
    # model_predict = contract_analysis(contract_articles)

    print(splited_contract_doc)

    return render_template('check.html')

if __name__ == '__main__':
    app.run()
