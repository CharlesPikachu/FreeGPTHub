'''
Function:
    Implementation of BaiduQianfanEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import HighflyerDeepSeekEndpoints, ChatRequest


# prepare questions for deepseek
req = ChatRequest(text='5 * 9 = ?')
# test all models
deepseek_client = HighflyerDeepSeekEndpoints()
resp = deepseek_client.send(req=req, version='deepseek-chat')
print(resp.text)
resp = deepseek_client.send(req=req, version='deepseek-v3')
print(resp.text)