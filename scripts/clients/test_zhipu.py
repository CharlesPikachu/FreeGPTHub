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


# prepare questions for zhipu
req = ChatRequest(text='How to calculate 100 * 20 / 30')
# test all models
glm_client = ZhipuGLMEndpoints()
resp = glm_client.send(req=req, version='glm-4-flash')
print(resp.text)
time.sleep(10)
resp = glm_client.send(req=req, version='glm-4.5-flash')
print(resp.text)