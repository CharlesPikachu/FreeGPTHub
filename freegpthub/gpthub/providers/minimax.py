'''
Function:
    Implementation of MiniMaxEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import secrets
from .base import BaseEndpoint
from typing import Union, Dict, Any, Optional
from ..utils import ChatRequest, ChatResponse, ModelIOType, StreamSanitizer


'''SETTINGS'''
MINIMAX_SHARED_KEYS = [
    'RxSEewtC765SQ2a31yZz-jfVWc2n_N53k0MhVxtmHEJtpipRsdLE_7qWBROHslXTbUHXo2-7MowCk-eCZC4uFnn0f6l_1eZodKcLL2-fwFjpwKO8ZzXh7qQYUCciAMM845IdQ_nqGa-etULLGkcjqj1RBlVraohWHwgE_qqAERLCnjj4IWclKXWCBo4O1krmUjj-9nE_CDWwnERCiPBDy1lnx7c3wH2dL-H7yg5rJ55CqMhhwkpy0UHGMedjAF3MGU119ptN-2Ravu0pFuUNJeSMzyWl7bbnqoNjb-leGAAbl8exsrDWBPVvo1q59P5Yo3wu7QI59liUY6l9xmNoyV_25UxO5xI696pyQKdiql9xtgkkalVomAXZ2aHJkZ97V4ZAdH9gpe0hGHG3Q2BAS3XQAnhVAxxWxDL1VoyS9tG--ZDjc0Z0XuGWLccT1CZFxc0o6NQOx2SJ9fqiZgHi9vRqjbCjAroSTfdc4zhbu3iemfRFupOqHNP-uBLUazrQvtkCiH5m_fydC0HASXgnrv8mzcxskqcT50bgaNcGCNNWNGl_PgMJ1K_RCoZdw16gFY_fvG4kBkWOKZZyfBdFCMwiCFEK09q4kKs6aOt-LhHyplA6FxcWFLEBDw_zM1-BEYXR7nUFFQwsOfZWFox5G8AACkxiIl_rLFcTSIgMV2EPEHpin91wqOBBfjv5MuIOeXyoit35L7CLekm45k2hIPgoh72lbbplv_NLQK93wseSuVAz9Q6cUis5tu82HVCC0fOr7KjI0HvT7ECi_b9iuTV4i5wxF2wa23uC9cfRWPLn84ROLw3rMjTqinKh_q1E6z8k66Hc75J0HCA574s_sHL7HUL33GQbZyorhP1kTQhe6__mQTvPj6_iwvhPHIGgfnS2YgA5x8nHFU6GlxzdVGw-HtsC82h82NE1mbcpjc349yDIxlBTUxvp_iAMyVyzBSJBZQLvIeRBArC6CeKEtOxkCLNHdPgg04MRYYtmS94goA5UP80xqVyQTKdnbCunnT0DCx4JeBOrD7fO-PQ8bZ7RmYfPRT4qCsvGFkDQFoYanNhCqNIqlOd4Cim1JgElHdJn9UlKXgyNYM_UMaDcpgEzhvuS2cxexoOEFaVrzRQMhJPK82JQWSsSUyn0Gx8y4pgu4nzSNDb0A23qzUii2oZT06gfwKSHlrAQeWL3prtSGGnKMcMc77n6MHU3NixBvVJN3waItMYlVINfaCMaA_fpcijMWlnTmepCToYVo9KBP88dE4NOTtd0fznTgkG8',
]
MINIMAX_FREE_API_KEYS = {
    'MiniMax-M2': MINIMAX_SHARED_KEYS, 'MiniMax-M2-Stable': MINIMAX_SHARED_KEYS,
}
MINIMAX_SCNET_FREE_API_KEYS = {
    'MiniMax-Text-01-456B': '8', 'MiniMax-M1-456B': '10', 
}


'''MiniMaxEndpoints'''
class MiniMaxEndpoints(BaseEndpoint):
    provider, model = "minimaxi", "minimaxi"
    def __init__(self, **kwargs):
        super(MiniMaxEndpoints, self).__init__(**kwargs)
        for ver in list(MINIMAX_FREE_API_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="officialapiv1", io=ModelIOType.fromtag("T2T"), handler="officialapiv1",
                priority=100, note='official api: https://api.minimaxi.com/v1'
            )
        for ver in list(MINIMAX_SCNET_FREE_API_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="scnetapiv1", io=ModelIOType.fromtag("T2T"), handler="scnetapiv1",
                priority=10, note='thirdpart api: https://www.scnet.cn/acx/chatbot/v1/chat/completion'
            )
    '''officialapiv1'''
    def officialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://api.minimaxi.com/v1', candidate_api_keys=MINIMAX_FREE_API_KEYS, api_family='client.chat.completions.create',
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
        payload['modelId'] = MINIMAX_SCNET_FREE_API_KEYS[version]
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