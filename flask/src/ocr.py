import os
import re
import asyncio
import io
import requests
import uuid
import time
import json
from functools import partial
from src.utils import load_conf
from src.pdf_split import PDFSplit

async def convert_to_text(file_name, file_extension, file_data, semaphore):
    conf = load_conf()
    api_url = conf['clova']['url']
    secret_key = conf['clova']['secret']

    request_json = {
        'images': [
            {
                'format': file_extension,
                'name': file_name + '_data'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
        ('file', file_data)
    ]
    headers = {
        'X-OCR-SECRET': secret_key
    }

    async with semaphore:
        request = partial(requests.post, api_url, headers=headers, data=payload, files=files)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, request)
        res = json.loads(response.text.encode('utf8'))

        return res

async def ocr_task(files):
    semaphore = asyncio.Semaphore(2)

    _, file_extension = os.path.splitext(files[0].filename)
    file_bytes = []
    if file_extension == '.pdf':
        pdf_obj = PDFSplit(files[0])
        file_bytes = pdf_obj.page_split()
    else:
        file_bytes = [io.BytesIO(f.read()) for f in files]

    result = []
    tasks = [asyncio.ensure_future(convert_to_text(str(idx), file_extension[1:], data, semaphore)) for idx, data in enumerate(file_bytes)]
    result = await asyncio.gather(*tasks)

    return result

def merge(json_list):
    contract_doc = ""
    for json_data in json_list:

        if not json_data.get('images'):
            return None
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