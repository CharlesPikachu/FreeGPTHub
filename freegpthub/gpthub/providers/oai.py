'''
Function:
    Implementation of OpenAIChatGPTEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from .base import BaseEndpoint
from ..utils import ChatRequest, ChatResponse, ModelIOType, Modality


'''SETTINGS'''
CHATGPT_FREE_API_KEYS = {
    'gpt-4o': [],
    'gpt-4o-mini': [],
}
CHATGPT_ANYWHERE_FREE_SHARED_KEYS = [
    'jw30KfjhzWiCv_ebwm3R5hRLVOX8IY9fvWUgHsL25Uj4qmv6XXFuuUOQWMOrJS5NDy5uLcwenJZ59Z3I4H8UkT0CnOU_UKE41K41qSkOm9qu5jg_G4sRWreeguM8MSTb', 
    '6sNVVAwcrhBAP0IJ5E06lrgevg4o2QSn_ibLLXdsXZjUkWdYwKxTOOkCn7dhS3luhVyd-UACwzjojOnOGrtaSnbodksrUU8fHUe91UiWzVJmi50GmOUDXV7s0cpF4hFE', 
    'BKTdCN1PTE3kOH9M28wnfAHO1au9WtjssL6zyH60mocGS-Hf8loZqH0Q2Bsp0DKr0-MGR6I7ms_yofpTQfR_wPkhTi5_hDfulXEm5lzH7CmNOBXKhL2xjWyxtQ3mbyuC', 
    'KLfM9uA3eVACCpXHBDGH1t1LARLRiOjHh8vpq0d3Vx8wV-jYQKIFggtw3XgdJA68VbJJzqflv6CnXG98a-GWQvxq_4Lf0kUr5dFVfraxdLV-1BnnAGJqR4wQgWoDQzWb', 
    'gJloHBPdzYBLaAWkRsdS9YP2HjyE2XLTmYZL6JQl2PfyeeCuSHmt8Q70015oWCHWFTP4dqc4eQwSmNEAoKmgVrI3JuhLbMtvz8VQIDffbsbig7UxfJgu4znZKEJh-R6i', 
    'plMXcvnACsKl6kxu1LDOdd6rVaqNBxhsper59meUf-Xf9RvOJ6B4ZqM8poKw5Vl1EsYPE9_UO5p9IF1Il7PMNzaNaX8irzyQoULZNqQbVMc-aP37iZmyWqe2y_UlTk7T', 
    'O23Drzh2YoDuAF1Yv8x2RDVLw2-wTNNYzB5jkaXf3Z4KBVQE6HLa-PxJRWvIb2k9CkXVszCbgufwNkUYqC-nvs9DqjmuOjDjui_cYSZ74yzXBcfOW3cL9GiaT_09LciX', 
    'TvSrB-wacUcTkYBUucmRlJT2afSf0ykv01wsog9xXSZOhfAiPG21w4SOtL7U_0p0_gLWXgN_GfLuuTaYnF7xssxr1sC13YsqNt0758DhaRx2d_CpxgQ5RDqx4W94HHsJ',
]
CHATGPT_ANYWHERE_FREE_API_V1_KEYS = {
    'gpt-5.2': CHATGPT_ANYWHERE_FREE_SHARED_KEYS, 'gpt-5.1': CHATGPT_ANYWHERE_FREE_SHARED_KEYS, 'gpt-5': CHATGPT_ANYWHERE_FREE_SHARED_KEYS,
    'gpt-4o': CHATGPT_ANYWHERE_FREE_SHARED_KEYS, 'gpt-4.1': CHATGPT_ANYWHERE_FREE_SHARED_KEYS, 'gpt-4o-mini': CHATGPT_ANYWHERE_FREE_SHARED_KEYS,
    'gpt-3.5-turbo': CHATGPT_ANYWHERE_FREE_SHARED_KEYS, 'gpt-4.1-mini': CHATGPT_ANYWHERE_FREE_SHARED_KEYS, 'gpt-4.1-nano': CHATGPT_ANYWHERE_FREE_SHARED_KEYS,
    'gpt-5-mini': CHATGPT_ANYWHERE_FREE_SHARED_KEYS, 'gpt-5-nano': CHATGPT_ANYWHERE_FREE_SHARED_KEYS,
}
CHATGPT_BIANXIE_FREE_API_V1_KEYS = {
    'gpt-4o': ['rXftowCdzp52RYbrejAJ17TkqTHqibdMBbaOsEbYLppnPONitvK7YqQQBcf9hWaiiv85TAgmWotshy4LOCqaBDn6ib10rOX9G4-jlq_qGQq3EZoRsMwsju0KEipRWRgK']
}
CHATGPT_GPTBESTVIP_FREE_API_V1_KEYS = {
    'gpt-4o-mini': ['S06SosGNrr-UaXY46KfjK-2sltumTl21BhuivUpdXp36ZDi7xnoCpebdmGHhTzpu_RZB6ZgBq0WfwPBJ45o9qH7GlrwZh43LD1eiPSgk0y2E1JreXxT20O3F2zx_0lqD'],
    'gpt-4o': ['S06SosGNrr-UaXY46KfjK-2sltumTl21BhuivUpdXp36ZDi7xnoCpebdmGHhTzpu_RZB6ZgBq0WfwPBJ45o9qH7GlrwZh43LD1eiPSgk0y2E1JreXxT20O3F2zx_0lqD'],
    'gpt-5.1': ['S06SosGNrr-UaXY46KfjK-2sltumTl21BhuivUpdXp36ZDi7xnoCpebdmGHhTzpu_RZB6ZgBq0WfwPBJ45o9qH7GlrwZh43LD1eiPSgk0y2E1JreXxT20O3F2zx_0lqD'],
    'gpt-5.2': ['S06SosGNrr-UaXY46KfjK-2sltumTl21BhuivUpdXp36ZDi7xnoCpebdmGHhTzpu_RZB6ZgBq0WfwPBJ45o9qH7GlrwZh43LD1eiPSgk0y2E1JreXxT20O3F2zx_0lqD'],
}


'''OpenAIChatGPTEndpoints'''
class OpenAIChatGPTEndpoints(BaseEndpoint):
    provider, model = "openai", "chatgpt"
    def __init__(self, **kwargs):
        super(OpenAIChatGPTEndpoints, self).__init__(**kwargs)
        T2T = ModelIOType.fromtag("T2T")
        TI2T = ModelIOType.create(inputs=[Modality.TEXT, Modality.IMAGE], outputs=[Modality.TEXT])
        for ver in list(CHATGPT_ANYWHERE_FREE_API_V1_KEYS.keys()):
            self.registervariant(ver, io_supported=[T2T, TI2T] if ver not in ['gpt-3.5-turbo'] else [T2T])
            self.registerapi(version=ver, name="chatanywhereapiv1", io=T2T, handler="chatanywhereapiv1", priority=10, note='thirdpart api: https://api.chatanywhere.tech/v1')
        for ver in list(CHATGPT_BIANXIE_FREE_API_V1_KEYS.keys()):
            self.registervariant(ver, io_supported=[T2T, TI2T])
            self.registerapi(version=ver, name="bianxieapiv1", io=T2T, handler="bianxieapiv1", priority=11, note='thirdpart api: https://api.bianxie.ai/v1')
            self.registerapi(version=ver, name="visionbianxieapiv1", io=TI2T, handler="visionbianxieapiv1", priority=11, note='thirdpart api: https://api.bianxie.ai/v1')
        for ver in list(CHATGPT_GPTBESTVIP_FREE_API_V1_KEYS.keys()):
            self.registervariant(ver, io_supported=[T2T, TI2T])
            self.registerapi(version=ver, name="gptbestvipapiv1", io=T2T, handler="gptbestvipapiv1", priority=11, note='thirdpart api: https://hk-api.gptbest.vip/v1')
            self.registerapi(version=ver, name="visiongptbestvipapiv1", io=TI2T, handler="visiongptbestvipapiv1", priority=11, note='thirdpart api: https://hk-api.gptbest.vip/v1')
    '''chatanywhereapiv1'''
    def chatanywhereapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://api.chatanywhere.tech/v1', candidate_api_keys=CHATGPT_ANYWHERE_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''bianxieapiv1'''
    def bianxieapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://api.bianxie.ai/v1', candidate_api_keys=CHATGPT_BIANXIE_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''visionbianxieapiv1'''
    def visionbianxieapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.visionopenaisdk(
            base_url='https://api.bianxie.ai/v1', candidate_api_keys=CHATGPT_BIANXIE_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''gptbestvipapiv1'''
    def gptbestvipapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://hk-api.gptbest.vip/v1', candidate_api_keys=CHATGPT_GPTBESTVIP_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''visiongptbestvipapiv1'''
    def visiongptbestvipapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.visionopenaisdk(
            base_url='https://hk-api.gptbest.vip/v1', candidate_api_keys=CHATGPT_GPTBESTVIP_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )