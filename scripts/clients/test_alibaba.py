'''
Function:
    Implementation of AlibabaQwenEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import ChatRequest, AlibabaQwenEndpoints


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for qwen I2I
req = ChatRequest(text='10 * 10 = ?')
# test text models
qwen_client = AlibabaQwenEndpoints(aes_gem_key=aes_gem_key)
resp = qwen_client.send(req=req, version='qwen-plus')
print(resp.text)
resp = qwen_client.send(req=req, version='Qwen3-30B-A3B')
print(resp.text)
resp = qwen_client.send(req=req, version='Qwen3-235B-A22B')
print(resp.text)

# prepare questions for qwen TI2T
req = ChatRequest(text='Describe the image?', images=('https://raw.githubusercontent.com/CharlesPikachu/FreeGPTHub/main/docs/dog.jpeg',))
# test vision model
qwen_client = AlibabaQwenEndpoints(aes_gem_key=aes_gem_key)
resp = qwen_client.send(req=req, version='qwen3-vl-plus')
print(resp.text)