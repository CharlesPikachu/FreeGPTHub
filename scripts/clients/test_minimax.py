'''
Function:
    Implementation of MiniMaxEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import ChatRequest, MiniMaxEndpoints


# prepare questions for minimax I2I
req = ChatRequest(text='10 * 10 = ?')
# test text models
minimax_client = MiniMaxEndpoints()
resp = minimax_client.send(req=req, version='MiniMax-Text-01-456B')
print(resp.text)
resp = minimax_client.send(req=req, version='MiniMax-M1-456B')
print(resp.text)
resp = minimax_client.send(req=req, version='MiniMax-M2')
print(resp.text)