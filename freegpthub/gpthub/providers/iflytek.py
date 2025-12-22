'''
Function:
    Implementation of IFLYTEKSparkEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import hmac
import json
import base64
import random
import hashlib
import websocket
from time import mktime
from datetime import datetime
from .base import BaseEndpoint
from urllib.parse import urlencode, urlparse
from wsgiref.handlers import format_date_time
from ..utils import resp2json, ChatRequest, ChatResponse, ModelIOType, SecretUtils


'''SETTINGS'''
SPARK_FREE_APIV1_KEYS = {
    'lite': [
        'BrQGpZuyF-r-aa8BsEcILHhyck6bRGmeW5tOjGlKwLNkKeU04juloTRFZP7GtRlDWcU4hPcHtTycdJfRfcktr1JWlj54hlfnTe7bbbKl-FprpUcj',
        'D9-CjAmX4ww-_QFr_s9BLQ1fHoq60aHZ46-ATnsHL4JeO5_0GeQeEKP9Di337RQ1n2VQz0U-MhNZcaMn7XN-v_MJDkhQ9zIONBCkstyOyvgRePzp', 
    ],
    '4.0Ultra': [
        {'app_id': 'z8LR_zVlO-rnQzbiO_LoXe8wx4iPjRkFAegZ57flf1Xs6LIKwI4o2A==', 'api_key': '7fgq2apXPXAMJZ7t9ECF6st-jKQPxflqgaj7Z276GWgZkV_zivo-0SY4a0aIzD9-ZT-mBWLMBd9Eq2s8-NpBpI5Dx1UcSFfg', 'api_secret': 'Ly3BhBZeA19xT_D2HBlOhklLUw7JsljAJM1Cr4M9Z-JFQv_9O12ZQsPlp4FMy_9MNNxM8zmHnAMDqm8oQsiimUyL-h-CsNMw'}
    ],
}


'''IFLYTEKSparkEndpoints'''
class IFLYTEKSparkEndpoints(BaseEndpoint):
    provider, model = "iflytek", "spark"
    def __init__(self, **kwargs):
        super(IFLYTEKSparkEndpoints, self).__init__(**kwargs)
        self.registervariant("lite", io_supported=[ModelIOType.fromtag("T2T")])
        self.registerapi(
            version="lite", name="cggapi", io=ModelIOType.fromtag("T2T"), handler="cggapi",
            priority=10, note='thirdparty api: https://api.cenguigui.cn/api/chat/?msg=',
        )
        self.registerapi(
            version="lite", name="officialapiv1", io=ModelIOType.fromtag("T2T"), handler="officialapiv1",
            priority=100, note='official api: https://spark-api-open.xf-yun.com/v1'
        )
        self.registervariant("4.0Ultra", io_supported=[ModelIOType.fromtag("T2T")])
        self.registerapi(
            version="4.0Ultra", name="officialapiv4", io=ModelIOType.fromtag("T2T"), handler="officialapiv4",
            priority=100, note='official api: wss://spark-api.xf-yun.com/v4.0/chat'
        )
    '''officialapiv1'''
    def officialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://spark-api-open.xf-yun.com/v1', candidate_api_keys=SPARK_FREE_APIV1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''officialapiv4'''
    def officialapiv4(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        # init
        request_overrides = request_overrides or {}
        full_response, websocket_cfg = [], req.websocket
        # _buildauthurl
        def _buildauthurl(ws_url: str, api_key: str, api_secret: str) -> str:
            u = urlparse(ws_url)
            host, path = u.netloc, u.path
            date = format_date_time(mktime(datetime.now().timetuple()))
            signature_origin = f"host: {host}\n" f"date: {date}\n" f"GET {path} HTTP/1.1"
            signature_sha = hmac.new(api_secret.encode("utf-8"), signature_origin.encode("utf-8"), digestmod=hashlib.sha256).digest()
            signature = base64.b64encode(signature_sha).decode("utf-8")
            authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
            authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")
            params = {"authorization": authorization, "date": date, "host": host}
            return ws_url + "?" + urlencode(params)
        # _buildrequest
        def _buildrequest(websocket_cfg: dict, content: str, domain: str, app_id: str) -> dict:
            return {
                "header": {"app_id": app_id, "uid": "user_001"},
                "parameter": websocket_cfg.get('parameter') or {"chat": {"domain": domain, "temperature": 0.5, "top_k": 4, "max_tokens": 2048}},
                "payload": websocket_cfg.get('payload') or {"message": {"text": [{"role": "user", "content": content}]}},
            }
        # _onopen
        def _onopen(ws: websocket.WebSocketApp):
            payload = _buildrequest(content=req.text, domain=version, app_id=app_id, websocket_cfg=websocket_cfg)
            ws.send(json.dumps(payload, ensure_ascii=False))
        # _onmessage
        def _onmessage(ws: websocket.WebSocketApp, message):
            nonlocal full_response
            data: dict = json.loads(message)
            header: dict = data.get("header", {})
            if header.get("code", -1) != 0: raise RuntimeError(f"Spark error: {header}")
            payload: dict = data.get("payload", {})
            choices: dict = payload.get("choices", {})
            text_list: list[dict] = choices.get("text", [])
            if text_list:
                delta = text_list[0].get("content", "")
                if delta: full_response.append(delta)
            if header.get("status") == 2: ws.close()
        # _onerror
        def _onerror(ws, error): print("\n[ws error]", error)
        # _onclose
        def _onclose(ws, close_status_code, close_msg): pass
        # obtain api info
        app_secret = random.choice(SPARK_FREE_APIV1_KEYS[version])
        app_id = SecretUtils.b64decode(SecretUtils.decryptaesgcm(app_secret['app_id'], self.aes_gem_key))
        api_key = SecretUtils.b64decode(SecretUtils.decryptaesgcm(app_secret['api_key'], self.aes_gem_key))
        api_secret = SecretUtils.b64decode(SecretUtils.decryptaesgcm(app_secret['api_secret'], self.aes_gem_key))
        # websocket
        ws_final_url = _buildauthurl("wss://spark-api.xf-yun.com/v4.0/chat", api_key, api_secret)
        ws = websocket.WebSocketApp(ws_final_url, on_open=_onopen, on_message=_onmessage, on_error=_onerror, on_close=_onclose)
        ws.run_forever(sslopt={"check_hostname": True})
        # return
        return ChatResponse(text="".join(full_response), raw=full_response)
    '''cggapi'''
    def cggapi(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        request_overrides = request_overrides or {}
        try:
            resp = self.session.get("https://api.cenguigui.cn/api/chat/", params={"msg": req.text}, **request_overrides)
            resp.raise_for_status()
        except:
            resp = self.session.get("https://api-v1.cenguigui.cn/api/chat/", params={"msg": req.text}, **request_overrides)
            resp.raise_for_status()
        api_resp_raw_data = resp2json(resp)
        return ChatResponse(text=api_resp_raw_data['data']['content'], raw=api_resp_raw_data)