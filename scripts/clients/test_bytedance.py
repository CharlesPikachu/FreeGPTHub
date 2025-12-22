'''
Function:
    Implementation of ByteDanceDoubaoEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import ByteDanceDoubaoEndpoints, ChatRequest


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for doubao T2T
req = ChatRequest(text='5 * 9 = ?')
# test text models
doubao_client = ByteDanceDoubaoEndpoints(aes_gem_key=aes_gem_key)
resp = doubao_client.send(req=req, version='doubao')
print(resp.text)
resp = doubao_client.send(req=req, version='doubao-seed-1-6-251015')
print(resp.text)