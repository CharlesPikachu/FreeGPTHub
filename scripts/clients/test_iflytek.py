'''
Function:
    Implementation of IFLYTEKSparkEndpoints Tester
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from freegpthub.gpthub import ChatRequest, IFLYTEKSparkEndpoints


# prepare questions for spark
req = ChatRequest(text='10 * 10 = ?')
# test all models
spark_client = IFLYTEKSparkEndpoints()
resp = spark_client.send(req=req, version='lite')
print(resp.text)