'''
Function:
    Implementation of Common Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import requests
import json_repair


'''resp2json'''
def resp2json(resp: requests.Response):
    if not isinstance(resp, requests.Response): return {}
    try:
        result = resp.json()
    except:
        result = json_repair.loads(resp.text)
    if not result: result = dict()
    return result