'''
Function:
    Implementation of BaiduQianfanEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from .base import BaseEndpoint
from ..utils import ChatRequest, ChatResponse, ModelIOType


'''SETTINGS'''
QIANFAN_SHARED_KEYS = [
    'oiP1BpFuiPBfnyHJm9i5TAgwMZG3Y0Vd8UBqTmxaS2M7MNVHtz14eNsaOKa5n2T-2DDthiKYFZU25JAzlgUAECa4KIrn5s08Xete_El9TPTOTDPTvzsQaDpE-5JSrTYYrmPaWgmp7hYcfEIhYk9nsl62zhMcBLIk_7gXV9AXfb8=', 
    'DTeSqHsTdBZthSJfrAR575nGNh4ZGNk0Jz-hU5YrMZicCeJuxUJDO9YJACGcTD9UQ60f41eYwv3Gl6okp7hT3LYHTClIApx_nsOSVty2_D-BViS9qTqkQuh-ZZZSZOfWrBtglkl7I03ZQW6o1bug3uq75HEjtBMeK-dWtQJTlvE=', 
    'mHXHSnXsn562akeQfJDEvheYzdMtzVXuhLh-I8_NRjn5_yB0R8zGZpWaXM7rlN8SbL-kneABpK5FsMWWMm2X0ClHX3qqBjFGALf6EXzcpuIj6H2wcyklxHmn0i2AZnaGpxffSKuyoARrgY0lmokpMI0o_1OoxHbIeykhoyCW7R8='
]
QIANFAN_FREE_API_V2_KEYS = {
    'deepseek-v3': QIANFAN_SHARED_KEYS, 'ernie-4.0-turbo-8k': QIANFAN_SHARED_KEYS,
}


'''BaiduQianfanEndpoints'''
class BaiduQianfanEndpoints(BaseEndpoint):
    provider, model = "baidu", "qianfan"
    def __init__(self, **kwargs):
        super(BaiduQianfanEndpoints, self).__init__(**kwargs)
        for ver in list(QIANFAN_FREE_API_V2_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="officialapiv2", io=ModelIOType.fromtag("T2T"), handler="officialapiv2",
                priority=100, note='official api: https://qianfan.baidubce.com/v2'
            )
    '''officialapiv2'''
    def officialapiv2(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://qianfan.baidubce.com/v2', candidate_api_keys=QIANFAN_FREE_API_V2_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )