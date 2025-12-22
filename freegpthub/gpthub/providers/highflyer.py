'''
Function:
    Implementation of HighflyerDeepSeekEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from .base import BaseEndpoint
from ..utils import ChatRequest, ChatResponse, ModelIOType


'''SETTINGS'''
DEEPSEEK_FREE_API_KEYS = {
    'deepseek-chat': [
        'iWSTxC-YSd4nupox9dX6Y4DeuEYHCvUrHRpsRbDDuQ9Ek2wG0eH8VjK-QvmHVTXhlthPqcvAfAPfmSIjSlQJ4x-ydYEqQdyKYCCqjQ==',
    ],
}
DEEPSEEK_ALIYUNCS_FREE_SHARED_KEYS = [
    'eFCw8sVzThf5PlQAfGP6rEU-DWTz8h-OOUxuoPuzwMNHTcY9RwEljO87aqFXsa8v8NRZxIoNxJrWSLnipkMSQQLQi8dB85b7cpezFg==', 
    'L7XiMAoZGuVmbsWJ4mKoV7OySWFKl-ZM599F0-C_ZA3gQyj1TlB5L2fILq_l8hyonltIv53Bpk_xTWVJKWfRBmU3oyi0Msdr4ek-GQ==', 
    'VkS9va4uhcBBAMh8nJo0PhrLBl6H1BlLv4HQp1wpVZpYzz4qhhAH0ePOQaIJFEh7rgT3Y4pvgUnx5QrLmIN255sup3pcK5Tlk3l19Q==', 
    'DGT_SCWxaDnV3DouSk-TBKqg7sRVztPCuOtW2sgdAvKkk0vZzAeklOAj51YhH-2hKAhvHxM0DhpVBozafSdCrhiW-e3xsaBZ79Bu7g==', 
    'wZhgD2y9dYHO_xX2B1bil25qpl0w0pZ0sbyX9GhCDwamRVSMBJUeKYg4Ssd8YyZsp7xTshkUBOGr5KiGmXB4ZC6Fk87Ff6hV-yZONw==', 
    'oW1la7eBruvbYUSlO8q3tESc_FPGGoKKLxFXi12HfL1JVhF-c5ShfxNSY2qkKMsJwFI3ffzZ40QiYGOJqNgi2zagFyEKArhdGKRHeQ==', 
    'q50HVPVK5tBh0yq32a1-7xCxczVqyNIacwRPZy0OEUZYd4FDqW1B1ey9hAn4lVO3Rb7z8_nacbREU7eotkeFnQDhiWtFhP1UUS8Rag==',
]
DEEPSEEK_ALIYUNCS_FREE_API_V1_KEYS = {
    'deepseek-v3': DEEPSEEK_ALIYUNCS_FREE_SHARED_KEYS, 'deepseek-r1': DEEPSEEK_ALIYUNCS_FREE_SHARED_KEYS, 'deepseek-v3.1': DEEPSEEK_ALIYUNCS_FREE_SHARED_KEYS,
    'deepseek-v3.2': DEEPSEEK_ALIYUNCS_FREE_SHARED_KEYS, 'deepseek-v3.2-exp': DEEPSEEK_ALIYUNCS_FREE_SHARED_KEYS,
}
DEEPSEEK_QIANFAN_FREE_SHARED_KEYS = [
    'oiP1BpFuiPBfnyHJm9i5TAgwMZG3Y0Vd8UBqTmxaS2M7MNVHtz14eNsaOKa5n2T-2DDthiKYFZU25JAzlgUAECa4KIrn5s08Xete_El9TPTOTDPTvzsQaDpE-5JSrTYYrmPaWgmp7hYcfEIhYk9nsl62zhMcBLIk_7gXV9AXfb8=', 
    'DTeSqHsTdBZthSJfrAR575nGNh4ZGNk0Jz-hU5YrMZicCeJuxUJDO9YJACGcTD9UQ60f41eYwv3Gl6okp7hT3LYHTClIApx_nsOSVty2_D-BViS9qTqkQuh-ZZZSZOfWrBtglkl7I03ZQW6o1bug3uq75HEjtBMeK-dWtQJTlvE=', 
    'mHXHSnXsn562akeQfJDEvheYzdMtzVXuhLh-I8_NRjn5_yB0R8zGZpWaXM7rlN8SbL-kneABpK5FsMWWMm2X0ClHX3qqBjFGALf6EXzcpuIj6H2wcyklxHmn0i2AZnaGpxffSKuyoARrgY0lmokpMI0o_1OoxHbIeykhoyCW7R8='
]
DEEPSEEK_QIANFAN_FREE_API_V2_KEYS = {'deepseek-v3': DEEPSEEK_QIANFAN_FREE_SHARED_KEYS}


'''HighflyerDeepSeekEndpoints'''
class HighflyerDeepSeekEndpoints(BaseEndpoint):
    provider, model = "high-flyer", "deepseek"
    def __init__(self, **kwargs):
        super(HighflyerDeepSeekEndpoints, self).__init__(**kwargs)
        for ver in list(DEEPSEEK_FREE_API_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="officialapi", io=ModelIOType.fromtag("T2T"), handler="officialapi",
                priority=100, note='official api: https://api.deepseek.com'
            )
        for ver in list(DEEPSEEK_ALIYUNCS_FREE_API_V1_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="aliyuncsapiv1", io=ModelIOType.fromtag("T2T"), handler="aliyuncsapiv1",
                priority=10, note='thirdpart api: https://dashscope.aliyuncs.com/compatible-mode/v1'
            )
        for ver in list(DEEPSEEK_QIANFAN_FREE_API_V2_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="qianfanapiv2", io=ModelIOType.fromtag("T2T"), handler="qianfanapiv2",
                priority=10, note='thirdpart api: https://qianfan.baidubce.com/v2'
            )
    '''officialapi'''
    def officialapi(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://api.deepseek.com', candidate_api_keys=DEEPSEEK_FREE_API_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''aliyuncsapiv1'''
    def aliyuncsapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', candidate_api_keys=DEEPSEEK_ALIYUNCS_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''qianfanapiv2'''
    def qianfanapiv2(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://qianfan.baidubce.com/v2', candidate_api_keys=DEEPSEEK_QIANFAN_FREE_API_V2_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )