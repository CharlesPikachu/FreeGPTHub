'''
Function:
    Implementation of AlibabaQwenEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import secrets
from .base import BaseEndpoint
from typing import Union, Dict, Any, Optional
from ..utils import ChatRequest, ChatResponse, ModelIOType, Modality, StreamSanitizer


'''SETTINGS'''
QWEN_FREE_SHARED_KEYS = [
    'pG4WicNJC9wohzOPEg6kQcuag3xr5O9Uhe1VUf7J95Bvo9PhICkKqUR4jEJb83t3dpp6WYA7YRz3cW76o7Rns7ns9JDycckEBMpi-w==', 
    'LnML1ffAjOw0tInoedXkswF0nTGZQWh-Jnj_V_IBe05PSQcklAhNnjdLxcL0KTe--Sc85qRtQcfV7Zo-IdXwyrusJh-9njvTypGN5Q==', 
    'J6TXvPOvm7rMjGecgG3yta9OUSt7FRt2ao4bOaKMjlX2TMLiuSd0YXDiDWw-3k5WXRWAWh5z-s0xpo0DVhoyqnLWlCjujVe5Q0im2w==', 
    'AW9ZCVKq9Yycu2xlmrozwgZyXCKagE8MayrbedteSdLZ01Hhwl1yL9MTPUxxtfdpQr7m1QxvNY2j3jAc1i8UcEPGLyh0_lY9j31EwQ==', 
    'MyZsP9AJmtZeqxoxH1nV7LQ8zmikWJhc4hQfqf-XARa9Lmd9VJ04RikkPbv6WW_qzfWAxvbT_L1fc3wVBVbXT2o3McMCFxZL2n6mgw==', 
    '96q5jwtx1b-kNh6X-0m6OVB3yMIMIfQibrk3T7X6SGVlEJ_pHmKtB6CHq_inDKqg2MPRCoFtteqM3y1Y0RqX3Vcbeks5DPardB4JAw==', 
    '3RJVZBVB33R7elL8c7wFTSnwmnfSCwirGcUA1Xkku9xUtM4f78PNzCElAtjLhJ9ApVAh4JxjbVsdGMCcvvOepUT_1Q-Z1nmhfi4qQA=='
]
QWEN_FREE_API_V4_KEYS = {
    'qwen-plus': QWEN_FREE_SHARED_KEYS, 'qwen3-max': QWEN_FREE_SHARED_KEYS, 'qwen-flash': QWEN_FREE_SHARED_KEYS, 'qwen-turbo': QWEN_FREE_SHARED_KEYS,
    'qwen-long': QWEN_FREE_SHARED_KEYS, 'qwen3-omni-flash': QWEN_FREE_SHARED_KEYS, 'qwen-math-plus': QWEN_FREE_SHARED_KEYS, 'qwen-math-turbo': QWEN_FREE_SHARED_KEYS,
    'qwen3-coder-plus': QWEN_FREE_SHARED_KEYS, 'qwen3-coder-flash': QWEN_FREE_SHARED_KEYS, 'qwen-mt-plus': QWEN_FREE_SHARED_KEYS, 'qwen-mt-flash': QWEN_FREE_SHARED_KEYS,
    'qwen-mt-lite': QWEN_FREE_SHARED_KEYS, 'qwen-mt-turbo': QWEN_FREE_SHARED_KEYS, 'qwen-doc-turbo': QWEN_FREE_SHARED_KEYS, 'qwen-deep-research': QWEN_FREE_SHARED_KEYS,
    'qwen3-vl-plus': QWEN_FREE_SHARED_KEYS, 'qwen3-vl-flash': QWEN_FREE_SHARED_KEYS, 'qwen-vl-max': QWEN_FREE_SHARED_KEYS, 'qwen-vl-ocr': QWEN_FREE_SHARED_KEYS,
}
QWEN_SCNET_FREE_API_KEYS = {
    'Qwen3-30B-A3B': '9', 'Qwen3-235B-A22B': '120', 
}


'''AlibabaQwenEndpoints'''
class AlibabaQwenEndpoints(BaseEndpoint):
    provider, model = "alibaba", "qwen"
    def __init__(self, **kwargs):
        super(AlibabaQwenEndpoints, self).__init__(**kwargs)
        TI2T = ModelIOType.create(inputs=[Modality.TEXT, Modality.IMAGE], outputs=[Modality.TEXT])
        for ver in list(QWEN_FREE_API_V4_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")] if '-vl-' not in ver else [ModelIOType.fromtag("T2T"), TI2T])
            self.registerapi(
                version=ver, name="officialapiv1", io=ModelIOType.fromtag("T2T"), handler="officialapiv1",
                priority=100, note='official api: https://dashscope.aliyuncs.com/compatible-mode/v1'
            )
            if '-vl-' in ver: self.registerapi(
                version=ver, name="visionofficialapiv1", io=TI2T, handler="visionofficialapiv1", priority=100, note='official api: https://dashscope.aliyuncs.com/compatible-mode/v1'
            )
        for ver in list(QWEN_SCNET_FREE_API_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="scnetapiv1", io=ModelIOType.fromtag("T2T"), handler="scnetapiv1",
                priority=10, note='thirdpart api: https://www.scnet.cn/acx/chatbot/v1/chat/completion'
            )
    '''officialapiv1'''
    def officialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', candidate_api_keys=QWEN_FREE_API_V4_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''visionofficialapiv1'''
    def visionofficialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.visionopenaisdk(
            base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', candidate_api_keys=QWEN_FREE_API_V4_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''scnetapiv1'''
    def scnetapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        # init
        request_overrides, cookies = request_overrides or {}, {"Token": secrets.token_hex(16)}
        headers = {
            "accept": "text/event-stream", "content-type": "application/json", "referer": "https://www.scnet.cn/", "origin": "https://www.scnet.cn",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        }
        # _scnetextractor
        def _scnetextractor(chunk: Union[str, Dict[str, Any]]) -> Optional[str]:
            if isinstance(chunk, dict): return chunk.get("content")
            return None
        # payload
        payload = {
            "conversationId": "", "content": "", "thinkingEnable": False, "onlineEnable": False, "modelId": "", "textFile": [], "imageFile": [], "clusterId": ""
        }
        for key in list(payload.keys()):
            if key in req.extra_payload: payload[key] = req.extra_payload[key]
        payload['content'] = req.text
        payload['modelId'] = QWEN_SCNET_FREE_API_KEYS[version]
        # post request
        resp = self.session.post("https://www.scnet.cn/acx/chatbot/v1/chat/completion", headers=headers, json=payload, stream=True, cookies=cookies, **request_overrides)
        resp.raise_for_status()
        # parse results
        processed_stream = StreamSanitizer(
            intro_value="data:", to_json=True, skip_markers=["[done]", "[DONE]"], content_extractor=_scnetextractor, yield_raw_on_error=False
        ).iter(data=resp.iter_content(chunk_size=None))
        streaming_text = ""
        for content_chunk in processed_stream:
            if content_chunk and isinstance(content_chunk, str):
                streaming_text += content_chunk
        streaming_text = streaming_text.strip().removesuffix('[done]').removesuffix('[DONE]')
        # return
        return ChatResponse(text=streaming_text, raw=resp)