'''
Function:
    Implementation of OpenAIChatGPTEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import OpenAIChatGPTEndpoints, ChatRequest


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for chatgpt T2T
req = ChatRequest(text='The area of China?')
# test text model
chatgpt_client = OpenAIChatGPTEndpoints(aes_gem_key=aes_gem_key)
resp = chatgpt_client.send(req=req, version='gpt-4o-mini')
print(resp.text)
resp = chatgpt_client.send(req=req, version='gpt-4o')
print(resp.text)


# prepare questions for chatgpt TI2T
req = ChatRequest(text='Describe the image?', images=('https://raw.githubusercontent.com/CharlesPikachu/FreeGPTHub/main/docs/dog.jpeg',))
# test vision model
chatgpt_client = OpenAIChatGPTEndpoints(aes_gem_key=aes_gem_key)
resp = chatgpt_client.send(req=req, version='gpt-4o')
print(resp.text)