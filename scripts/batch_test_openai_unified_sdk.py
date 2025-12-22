'''
Function:
    Implementation of OpenaiSDK
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from openai import OpenAI


'''settings'''
BASE_URL = ''
MODEL = ''
API_KEYS = []


'''iter to test'''
valids = []
for api_key in API_KEYS:
    try:
        client = OpenAI(base_url=BASE_URL, api_key=api_key)
        resp = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": "Hello, introduce yourself please."}])
        print(resp.choices[0].message.content)
        valids.append(api_key)
    except Exception as err:
        print(f'[Error]: {err}')
print(valids)