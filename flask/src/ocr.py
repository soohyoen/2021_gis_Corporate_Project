# 테서렉트
import pytesseract
import cv2
import numpy as np
import asyncio
from io import BytesIO

# 네이버 ocr
import requests
import uuid
import time
import json
import os
import re

# test를 위해서 tesseract로 이미지 전달하는 부분 체크
async def convert_to_text(image):
    npimg = np.fromstring(image.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    
    print(image.filename)
    # 데이터를 마치 파일로부터 읽을 것처럼 만들기
    # - 기존은 io.bufferedReader, image는 FileStorage
    # - 혹시라도 Clova OCR에서 문제가 생길가봐 형식 통일
    # img = BytesIO(image.read())

    result = []
    # 아래 부분을 Clova OCR로 대체
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(img, config=custom_config, lang='kor')

    return result


async def ocr_task(files):
    result = []
    # asyncio를 사용하긴 했지만, 현재 tesseract를 통한 ocr 처리 부분이 await가 없어서
    # 각 task들이 동기적으로 수행됨...
    # 이후 Clova OCR 요청으로 변경되면 해당 부분 await되면서 여러 요청이 동시에 보내질 것임
    tasks = [asyncio.create_task(convert_to_text(f)) for f in files]
    result = await asyncio.gather(*tasks)
    return result


# def naver_ocr():
#     api_url = ''
#     secret_key = ''

#     image_file = '계약서 스캔_{}.pdf'.format(x)
#     extension = os.path.splitext(image_file)[1]

#     request_json = {
#         'images': [
#             {
#                 'format': extension[1:],
#                 'name': image_file
#             }
#         ],
#         'requestId': str(uuid.uuid4()),
#         'version': 'V2',
#         'timestamp': int(round(time.time() * 1000))
#     }

#     payload = {'message': json.dumps(request_json).encode('UTF-8')}
#     files = [
#         ('file', open(image_file, 'rb'))
#     ]
#     headers = {
#         'X-OCR-SECRET': secret_key
#     }

#     response = requests.request("POST", api_url, headers=headers, data=payload, files=files)

#     res = json.loads(response.text.encode('utf8'))

#     return res

def merge(json_list):
    contract_doc = ""
    for json_data in json_list:
        data_fields = json_data['images'][0]['fields']

        for data in data_fields:
            _, _, text, _, _, is_linebreak = data.values()

            contract_doc += (' ' + text)
            if is_linebreak:
                contract_doc += "\n"

    return contract_doc


def split_article(document):
    result = []
    document = re.sub(r"[【】\[\]\(\),\{\}]", " ", document)

    p = re.compile('(\s?제\s?[0-9]+\s?조(\s|\[|\(|\{|\])[^제|규|\d])')
    pattern = re.compile('^제.+조$')

    split_doc = re.split(p, document)

    word = ""
    for idx, text in enumerate(split_doc):
        text = text.strip()
        if not text:
            continue

        if pattern.search(text):
            word = ''
        elif p.search(text):
            word = text[-1:]
        else:
            result.append((word if word else "") + text)
    return result