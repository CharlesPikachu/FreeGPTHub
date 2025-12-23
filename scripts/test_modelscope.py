'''
Function:
    Implementation of ModelScopeEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import ModelScopeEndpoints, ChatRequest


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for modelscope T2T
req = ChatRequest(text='The area of China?')
# test text model
modelscope_client = ModelScopeEndpoints(aes_gem_key=aes_gem_key)
resp = modelscope_client.send(req=req, version='deepseek-ai/DeepSeek-R1-0528')
print(resp.text)
resp = modelscope_client.send(req=req, version='Qwen/QVQ-72B-Preview')
print(resp.text)


# prepare questions for modelscope TI2T
req = ChatRequest(text='Describe the image?', images=('https://i0.hdslb.com/bfs/archive/fd33d7751737591ae0b6aa8663ece7f7bec88024.jpg',))
# test vision model
modelscope_client = ModelScopeEndpoints(aes_gem_key=aes_gem_key)
resp = modelscope_client.send(req=req, version='Qwen/Qwen2.5-VL-32B-Instruct')
print(resp.text)