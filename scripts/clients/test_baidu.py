'''
Function:
    Implementation of BaiduQianfanEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import BaiduQianfanEndpoints, ChatRequest


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for qianfan
req = ChatRequest(text='5 * 9 = ?')
# test all models
qianfan_client = BaiduQianfanEndpoints(aes_gem_key=aes_gem_key)
resp = qianfan_client.send(req=req, version='ernie-4.0-turbo-8k')
print(resp.text)