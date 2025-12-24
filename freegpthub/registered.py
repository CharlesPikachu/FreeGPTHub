'''
Function:
    Implementation of Registered Models
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from .gpthub import (
    EndpointRegistry, ModelScopeEndpoints, IFLYTEKSparkEndpoints, BaiduQianfanEndpoints, OpenAIChatGPTEndpoints, ZhipuGLMEndpoints,
    HighflyerDeepSeekEndpoints, ByteDanceDoubaoEndpoints, AlibabaQwenEndpoints, MiniMaxEndpoints,
)


'''REGISTERED_ENDPOINTS'''
REGISTERED_ENDPOINTS = EndpointRegistry()
REGISTERED_ENDPOINTS.register(ModelScopeEndpoints)
REGISTERED_ENDPOINTS.register(IFLYTEKSparkEndpoints)
REGISTERED_ENDPOINTS.register(BaiduQianfanEndpoints)
REGISTERED_ENDPOINTS.register(OpenAIChatGPTEndpoints)
REGISTERED_ENDPOINTS.register(ZhipuGLMEndpoints)
REGISTERED_ENDPOINTS.register(HighflyerDeepSeekEndpoints)
REGISTERED_ENDPOINTS.register(ByteDanceDoubaoEndpoints)
REGISTERED_ENDPOINTS.register(AlibabaQwenEndpoints)
REGISTERED_ENDPOINTS.register(MiniMaxEndpoints)