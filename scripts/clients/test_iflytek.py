'''
Function:
    Implementation of IFLYTEKSparkEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import ChatRequest, IFLYTEKSparkEndpoints


# aes_gem_key
aes_gem_key = eval(open('aes_gem_key.txt', 'r').read().strip())
print(aes_gem_key)
# prepare questions for spark
req = ChatRequest(text='10 * 10 = ?')
# test all models
spark_client = IFLYTEKSparkEndpoints(aes_gem_key=aes_gem_key)
resp = spark_client.send(req=req, version='lite')
print(resp.text)
resp = spark_client.send(req=req, version='4.0Ultra')
print(resp.text)