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
from ..utils import ChatRequest, ChatResponse, ModelIOType, StreamSanitizer, Modality


'''SETTINGS'''
MINIMAX_FREE_SHARED_KEYS = [
    'RxSEewtC765SQ2a31yZz-jfVWc2n_N53k0MhVxtmHEJtpipRsdLE_7qWBROHslXTbUHXo2-7MowCk-eCZC4uFnn0f6l_1eZodKcLL2-fwFjpwKO8ZzXh7qQYUCciAMM845IdQ_nqGa-etULLGkcjqj1RBlVraohWHwgE_qqAERLCnjj4IWclKXWCBo4O1krmUjj-9nE_CDWwnERCiPBDy1lnx7c3wH2dL-H7yg5rJ55CqMhhwkpy0UHGMedjAF3MGU119ptN-2Ravu0pFuUNJeSMzyWl7bbnqoNjb-leGAAbl8exsrDWBPVvo1q59P5Yo3wu7QI59liUY6l9xmNoyV_25UxO5xI696pyQKdiql9xtgkkalVomAXZ2aHJkZ97V4ZAdH9gpe0hGHG3Q2BAS3XQAnhVAxxWxDL1VoyS9tG--ZDjc0Z0XuGWLccT1CZFxc0o6NQOx2SJ9fqiZgHi9vRqjbCjAroSTfdc4zhbu3iemfRFupOqHNP-uBLUazrQvtkCiH5m_fydC0HASXgnrv8mzcxskqcT50bgaNcGCNNWNGl_PgMJ1K_RCoZdw16gFY_fvG4kBkWOKZZyfBdFCMwiCFEK09q4kKs6aOt-LhHyplA6FxcWFLEBDw_zM1-BEYXR7nUFFQwsOfZWFox5G8AACkxiIl_rLFcTSIgMV2EPEHpin91wqOBBfjv5MuIOeXyoit35L7CLekm45k2hIPgoh72lbbplv_NLQK93wseSuVAz9Q6cUis5tu82HVCC0fOr7KjI0HvT7ECi_b9iuTV4i5wxF2wa23uC9cfRWPLn84ROLw3rMjTqinKh_q1E6z8k66Hc75J0HCA574s_sHL7HUL33GQbZyorhP1kTQhe6__mQTvPj6_iwvhPHIGgfnS2YgA5x8nHFU6GlxzdVGw-HtsC82h82NE1mbcpjc349yDIxlBTUxvp_iAMyVyzBSJBZQLvIeRBArC6CeKEtOxkCLNHdPgg04MRYYtmS94goA5UP80xqVyQTKdnbCunnT0DCx4JeBOrD7fO-PQ8bZ7RmYfPRT4qCsvGFkDQFoYanNhCqNIqlOd4Cim1JgElHdJn9UlKXgyNYM_UMaDcpgEzhvuS2cxexoOEFaVrzRQMhJPK82JQWSsSUyn0Gx8y4pgu4nzSNDb0A23qzUii2oZT06gfwKSHlrAQeWL3prtSGGnKMcMc77n6MHU3NixBvVJN3waItMYlVINfaCMaA_fpcijMWlnTmepCToYVo9KBP88dE4NOTtd0fznTgkG8',
    'MTNRE4D0LSf6eyMsNEypUMfr05Zg2vj7j2RrlhGtNvLrbQbeSD5m_WyuDdZrywjAY1UPjrfow3RMW3Q3oLf-9pKa5RBL0kRNg3xA9M8No8CJ595m0E2FtDYx6gQ4HTfutUoMwfSvtDM6QHuiJuiqgvpsGnBIdCkSP2hHsT5rkQWRBm_CRKL2EgKibZZ3DjHhm4eViriqaPGW-NUvjjuaU-wrbJjuWRHZ4knC2k7juDQjWmJTsvT2JabHdEcO7DVEz7xKJVLEDFi2hcsVN1cdohnxxBg77FVvxqCh5fSOAv0_TIoEofFWv04lT3ENsZeI-pmvIUnc3xIepqh8-jl_TMSW1zDNJY92YSSSiDTgsCPXELIVDWTi3NZ6KIowKJVRjZbQzAVJmFC-BTsxAg3XRNqrjmu8GmbTQghgi64h82Ztx853-cgKXnQoOMfNNreLhCGKWGFsSm79GLYGCltkpmSO8afPkLzyvZ-pPK2DN3GGnidwkAue9vcw_vrPIwuSika3-TcClcZDoDMtJ3MAGcLttdW7_I80dtH7D6r1nkHzEXgMl5Dm6OwxdR45D8bENivc0gLmKvDsaCL9of4EIYE6NO3V_-OTT7pxvJ8m90HF-ou6AWUh9q056Eg4NUkUgIhEWvTtHss97dmfj93XsyVb4h4TCrvyp8ZyQIpFqrm_7eqQevn_J1PYHB47VFnNJDF2p1UBZgbt7C_5VUpe7aUROydnE6nfT-mRAsRifYdYKVGWjpGz-agWF08TBI7K-cmv2NMdPFMPPbCx48uEX5lDNaJOxpbf1zTvyPY4lY0R3f7KSzTtZiDweyldYSsin4sZuwg7XvOZtPkgO93xdYvsfIZyjDVw94eCeILad9fazu-EQi4rZK8ZLbtHeydKhhswXrHHC9okZ6L6yOFmbzxPZ91hchCY7ifuk4Ho5XB587rEJoKAD0_W4nFnv3qEQm3uJp4nxncUatzXOF4XmOpBH2nPz7chOt3dkkW_ieQQlSK65iJEiKTuZ-FXMiLpB2pU9vgOsMZwKjxfu-0HdPCjXMHsiKPsZQnlAtqn6jyJhzqgoYAmAzAMjvGt1KxcURJHhc1Q_CWquop3CGrzWY_ju1tLWTIAr7v4UfgBdY8jFU1FiwHp8hPu5iRbXuQOnacKb8kPGKCi_---eIM-1hrvjpD9M7vCiUG-o91ZAbki8Ibu9sP3bahfq-ZDvUMJS773Zfkl0orAzW4rhvBRpGLj5ruQWNrWH2jwmHOGEsOVSeMOn1Wisp4KyhVGNFyd',
    'j8CCnjWwc5UOxXdW_lfDFFvxnRIiGpPjIiWA0OKHPrCk6ba_GDGR051QsCm6C2UHPwe2PrCNA5BEfRST4CorwJbmuJUyBL2DqWikJ48KFqEdeQVU_KfKTfiGto47lFu4T2Z1OzOmAyxltdoNH3UCm9W9ehmFCvorvjIlyVgv3wKpc9ewkP3zhswLiaeW7_h0_SWMuY-qALzVliz693-uwteJ06Vj6Z8DzvyLeljb9YFkcTcb2dqleHVO55xoGj5uZTHaX38qg7vyjWLs9AP7FSyM9zavyTu-hm7G5tHMpMGbC99Z2iKX0Sn2m2cA4O_4CnG1JB0CEWn4D-fFumvnJLscWSw19cfoON2xX6eg6LUE9-98U1Z4UsChFHqpjgy3Uf_WQ7sTj9RZZrY0iH9T7rLN3Xdg0CP4Jer2C8J6Xl5DiYTFSVKyU_yIAzDSca3Y0nfZvlBWvZeoao_wAa1SpKqKJe0UR8wxLyai0_Efx_Bu5MSInSNwUgosphq3NyJUiOenPasMOQnKJXmS36FsQTQdFVpyL5fxqW5FgxkQ9oh43RfkDIz6iMNaZOq1r3bey2H5IDKKUQLQPFxx3g4U5ljFuywpBpP0icnnJrFuqGQ2cdFzg7nGO6ZIQPX3vLEU4dxOVkzmz_FnqT7lxeTA9F_gp1mUjdFamK4MDaS09uYo8HP7qWm6J76xbMrDtfa71A0mRujWGroRsCj2HN6OjMP13-P7b387tfDsPw79wsqIpwp6AuqgYscX4vJAetjJVMc-b0BkwWnOb2X_lx-1Qbjcxb3RlJA08Ir6Bqo32iJy-H8h6Q7fmzCcJlrcB2IZE5tDzoaaNMwPExj7kGLlS2z8Q4rytXHIqMWXqX6oc0WmWDOZzgtuzThPcbIvxLSuh8UzgCzTv0jSa_JuTTucjEM31_DcOmzJZ_Tl927Y2MVabCfPZJAzgmluJ9c8sOZOf1FF0Q_SIjIv6kxOTC-bB1r6ovG32b3U4DBFIWxjqEHc66MLDClUHuyIBcRtXQmVtOxrG08dTpFsleXed1XPhZkbIOvB4Ll2-HXbT_IwHjQO3-e808tBLfuqikr-dz2XL7VlMfZvF_V_LDxkezBfn6V2vuCYJ5c_1bomQTA2T6lY104QF5wQk2MPdQDgVRwpVtZzH-m4mfWy7j_JdroIyQ7uPbj3_r7WhnVFI_k-gJCjyxj38zlB6uwKSYo24-UrLTTw04o6QkJqJY5eKG31d9lA5_nzWnAMMIw6FQ95uQ2jujEQtelIfsFaj5rI3ykaEXs-4XBiayj4Qrxo',
]
MINIMAX_FREE_API_V1_KEYS = {
    'MiniMax-M2': MINIMAX_FREE_SHARED_KEYS, 'MiniMax-M2-Stable': MINIMAX_FREE_SHARED_KEYS, 'MiniMax-Text-01': MINIMAX_FREE_SHARED_KEYS[-1:]
}
MINIMAX_SCNET_FREE_API_V1_KEYS = {
    'MiniMax-Text-01-456B': '8', 'MiniMax-M1-456B': '10', 
}


'''MiniMaxEndpoints'''
class MiniMaxEndpoints(BaseEndpoint):
    provider, model = "minimaxi", "minimaxi"
    def __init__(self, **kwargs):
        super(MiniMaxEndpoints, self).__init__(**kwargs)
        TI2T = ModelIOType.create(inputs=[Modality.TEXT, Modality.IMAGE], outputs=[Modality.TEXT])
        for ver in list(MINIMAX_FREE_API_V1_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")] if ver in ['MiniMax-M2', 'MiniMax-M2-Stable'] else [ModelIOType.fromtag("T2T"), TI2T])
            self.registerapi(
                version=ver, name="officialapiv1", io=ModelIOType.fromtag("T2T"), handler="officialapiv1",
                priority=100, note='official api: https://api.minimaxi.com/v1'
            )
            if ver not in ['MiniMax-M2', 'MiniMax-M2-Stable']: self.registerapi(
                version=ver, name="visionofficialapiv1", io=TI2T, handler="visionofficialapiv1", priority=100, note='official api: https://api.minimaxi.com/v1'
            )
        for ver in list(MINIMAX_SCNET_FREE_API_V1_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="scnetapiv1", io=ModelIOType.fromtag("T2T"), handler="scnetapiv1",
                priority=10, note='thirdpart api: https://www.scnet.cn/acx/chatbot/v1/chat/completion'
            )
    '''officialapiv1'''
    def officialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://api.minimaxi.com/v1', candidate_api_keys=MINIMAX_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''visionofficialapiv1'''
    def visionofficialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.visionopenaisdk(
            base_url='https://api.minimaxi.com/v1', candidate_api_keys=MINIMAX_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
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
        payload['modelId'] = MINIMAX_SCNET_FREE_API_V1_KEYS[version]
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