'''
Function:
    Implementation of MiniMaxEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import ChatRequest, MiniMaxEndpoints


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for minimax I2I
req = ChatRequest(text='10 * 10 = ?')
# test text models
minimax_client = MiniMaxEndpoints(aes_gem_key=aes_gem_key)
resp = minimax_client.send(req=req, version='MiniMax-Text-01-456B')
print(resp.text)
resp = minimax_client.send(req=req, version='MiniMax-M1-456B')
print(resp.text)
resp = minimax_client.send(req=req, version='MiniMax-M2')
print(resp.text)

# test vision models
req = ChatRequest(text='Describe the image?', images=('https://raw.githubusercontent.com/CharlesPikachu/FreeGPTHub/main/docs/dog.jpeg',))
# test vision model
minimax_client = MiniMaxEndpoints(aes_gem_key=aes_gem_key)
resp = minimax_client.send(req=req, version='MiniMax-Text-01')
print(resp.text)