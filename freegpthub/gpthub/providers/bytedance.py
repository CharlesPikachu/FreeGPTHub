'''
Function:
    Implementation of ByteDanceDoubaoEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import random
from .base import BaseEndpoint
from ..utils import ChatRequest, ChatResponse, ModelIOType, Modality


'''SETTINGS'''
DOUBAO_ARK_FREE_API_V3_KEYS = {
    'doubao': [
        {'version': 'ep-20241224194233-9mshp', 'key': 'CP8yLN3fMBkBTKbkBbQ-BeGJFREg6Gmn4F9S-UdamYoYTV_KvmGXkBkQKk8HOLKJ62KK6UkuFqVfc2oSccFqmnQt3HHCquDSEOgLUA=='},
        {'version': 'ep-20250102142238-88hxn', 'key': 'dUfnths4KAdt6nf9GfqpkCUIX_dFvvK50p25ycKw-k0KvY9xdcIMDbbAP9214WVHHPoAEGOCNC-zG3Eo9R-uf-_hKYOQzVKgMsToJQ=='},
    ],
    'doubao-seed-1-6-251015': [
        {'version': 'doubao-seed-1-6-251015', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
    ],
    'doubao-1-5-pro-32k-250115': [
        {'version': 'doubao-1-5-pro-32k-250115', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
        {'version': 'doubao-1-5-pro-32k-250115', 'key': 'Fu2qVXf5NkhPn4ix9464ktl3HZryIyhQbioFk4_YwWcdaFWykFraXC6P5cPXa85v6elNOnJ-JUk_GptnQVuuEmRs94YNPCQLLDAeSA=='},
    ],
    'doubao-1-5-pro-32k-character-250715': [
        {'version': 'doubao-1-5-pro-32k-character-250715', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
    ],
    'doubao-1-5-pro-32k-character-250228': [
        {'version': 'doubao-1-5-pro-32k-character-250228', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
    ],
    'doubao-1-5-lite-32k-250115': [
        {'version': 'doubao-1-5-lite-32k-250115', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
    ],
    'doubao-seed-1-6-flash-250615': [
        {'version': 'doubao-seed-1-6-flash-250615', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
    ],
    'doubao-seed-1-6-flash-250715': [
        {'version': 'doubao-seed-1-6-flash-250715', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
    ],
    'doubao-seed-coder-250915': [
        {'version': 'doubao-seed-coder-250915', 'key': 'Ax08S1LZC-miCjDuWPTJ5MDI3EQs0PxY1udtOYFMr4lXfj1w0vibymwBXZiiu2W7kA1hpcRfJLt-0oSREM808nIVlJpAROL5xWJRFQ=='},
    ],
}


'''ByteDanceDoubaoEndpoints'''
class ByteDanceDoubaoEndpoints(BaseEndpoint):
    provider, model = "bytedance", "doubao"
    def __init__(self, **kwargs):
        super(ByteDanceDoubaoEndpoints, self).__init__(**kwargs)
        TI2T = ModelIOType.create(inputs=[Modality.TEXT, Modality.IMAGE], outputs=[Modality.TEXT])
        for ver in list(DOUBAO_ARK_FREE_API_V3_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="arkapiv3", io=ModelIOType.fromtag("T2T"), handler="arkapiv3",
                priority=10, note='thirdpart api: https://ark.cn-beijing.volces.com/api/v3'
            )
    '''arkapiv3'''
    def arkapiv3(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        vk = random.choice(DOUBAO_ARK_FREE_API_V3_KEYS[version])
        return self.openaisdk(
            base_url='https://ark.cn-beijing.volces.com/api/v3', candidate_api_keys={vk['version']: [vk['key']]}, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=vk['version']
        )