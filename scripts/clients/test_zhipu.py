'''
Function:
    Implementation of ZhipuGLMEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import time
from freegpthub.gpthub import ZhipuGLMEndpoints, ChatRequest


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for zhipu
req = ChatRequest(text='How to calculate 100 * 20 / 30')
# test all models
glm_client = ZhipuGLMEndpoints(aes_gem_key=aes_gem_key)
resp = glm_client.send(req=req, version='glm-4-flash')
print(resp.text)
time.sleep(10)
resp = glm_client.send(req=req, version='glm-4.5-flash')
print(resp.text)