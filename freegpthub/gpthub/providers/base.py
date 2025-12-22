'''
Function:
    Implementation of BaseEndpoint and EndpointRegistry
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import httpx
import base64
import random
import requests
from freeproxy import freeproxy
from openai import OpenAI, DefaultHttpxClient
from typing import Optional, Dict, Iterable, List, Any, Union, Tuple
from ..utils import ModelVariant, ChatRequest, ChatResponse, Modality, ModelIOType, APISpec, SecretUtils


'''BaseEndpoint'''
class BaseEndpoint:
    provider: str = "unknown"
    model: str = "unknown"
    def __init__(self, default_headers: dict = None, auto_set_proxies: bool = False,  proxy_sources: list = None, default_version: str = "default", aes_gem_key: bytes = None):
        assert aes_gem_key is not None, 'aes_gem_key is not set, so this library cannot be used. Please follow the WeChat official account "Charles的皮卡丘" and reply "FreeGPTHub" to obtain it.'
        # init session
        self.session = requests.Session()
        self.session.headers.update(default_headers or {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        })
        # set attributes
        self.aes_gem_key = aes_gem_key
        self.variants: Dict[str, ModelVariant] = {}
        self.auto_set_proxies = auto_set_proxies
        self.proxy_sources = proxy_sources
        self.default_version = default_version
        # proxied_session_client
        self.proxied_session_client = freeproxy.ProxiedSessionClient(
            proxy_sources=['GeonodeProxiedSession'] if proxy_sources is None else proxy_sources, 
            disable_print=True
        ) if auto_set_proxies else None
    '''registervariant'''
    def registervariant(self, version: str, io_supported: Iterable[ModelIOType]):
        if version in self.variants: return
        self.variants[version] = ModelVariant(provider=self.provider, model=self.model, version=version, io_supported=frozenset(io_supported), apis={})
    '''registerapi'''
    def registerapi(self, *, version: str, name: str, io: ModelIOType, handler: str, priority: int = 0, note: str = ""):
        if version not in self.variants: raise ValueError(f"Variant '{version}' not registered. Call registervariant() first.")
        if not hasattr(self, handler): raise AttributeError(f"Handler method '{handler}' not found on {self.__class__.__name__}")
        v = self.variants[version]
        v.apis[name] = APISpec(name=name, io=io, handler=handler, priority=priority, note=note)
    '''inferio'''
    def inferio(self, req: Any) -> ModelIOType:
        if isinstance(req, ChatRequest):
            in_mods: List[Union[Modality, str]] = [Modality.TEXT]
            if req.images: in_mods.append(Modality.IMAGE)
            return ModelIOType.create(inputs=in_mods, outputs=[Modality.TEXT])
        raise TypeError(f"Unsupported request type: {type(req)}")
    '''initopenaiclient'''
    def initopenaiclient(self, base_url: str, candidate_api_keys: dict, req: ChatRequest, version: str = None):
        openai_cfg: dict = req.openai
        if 'http_client' not in openai_cfg['client'] and self.auto_set_proxies:
            client = OpenAI(
                base_url=base_url, api_key=SecretUtils.b64decode(SecretUtils.decryptaesgcm(random.choice(candidate_api_keys[version]), self.aes_gem_key)), 
                http_client=DefaultHttpxClient(
                    proxy=self.proxied_session_client.getrandomproxy(proxy_format='freeproxy'), 
                    transport=httpx.HTTPTransport(local_address="0.0.0.0")
                ), **openai_cfg['client']
            )
        else:
            client = OpenAI(
                base_url=base_url, api_key=SecretUtils.b64decode(SecretUtils.decryptaesgcm(random.choice(candidate_api_keys[version]), self.aes_gem_key)), **openai_cfg['client']
            )
        return client
    '''openaisdk'''
    def openaisdk(self, base_url: str, candidate_api_keys: dict, api_family: str, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        # init
        request_overrides = request_overrides or {}
        openai_cfg: dict = req.openai
        # create client
        client = self.initopenaiclient(base_url=base_url, candidate_api_keys=candidate_api_keys, req=req, version=version)
        # specify model
        model_override = openai_cfg[api_family].pop('model', None)
        model = model_override or version
        # construct message
        messages_override = openai_cfg[api_family].pop('messages', None)
        messages = messages_override or [{"role": "user", "content": req.text}]
        # request based on api_family
        if api_family in ['client.chat.completions.create']:
            resp = client.chat.completions.create(model=model, messages=messages, **openai_cfg[api_family])
            text = self._extracttextfromchatcompletionsobj(resp)
            return ChatResponse(text=text, raw=resp.to_json() or resp)
        elif api_family in ['client.responses.create']:
            resp = client.responses.create(model=model, input=req.text, **openai_cfg[api_family])
            text = self._extracttextfromresponseobj(resp)
            raw = resp.model_dump() if hasattr(resp, "model_dump") else resp
            return ChatResponse(text=text, raw=raw)
        else:
            raise TypeError(f"Unsupported api_family: {api_family}")
    '''visionopenaisdk'''
    def visionopenaisdk(self, base_url: str, candidate_api_keys: dict, api_family: str, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        # init
        request_overrides = request_overrides or {}
        openai_cfg: dict = req.openai
        # create client
        client = self.initopenaiclient(base_url=base_url, candidate_api_keys=candidate_api_keys, req=req, version=version)
        # specify model
        model_override = openai_cfg[api_family].pop('model', None)
        model = model_override or version
        # construct message
        messages_override = openai_cfg[api_family].pop('messages', None)
        # request based on api_family
        if api_family in ['client.chat.completions.create']:
            images = getattr(req, "images", None) or ()
            content = [{"type": "text", "text": req.text}]
            for img in images: content.append({"type": "image_url", "image_url": {'url': self._imgtourl(img)}})
            messages = messages_override or [{"role": "user", "content": content}]
            resp = client.chat.completions.create(model=model, messages=messages, **openai_cfg[api_family])
            text = self._extracttextfromchatcompletionsobj(resp)
            return ChatResponse(text=text, raw=resp.to_json() or resp)
        elif api_family in ['client.responses.create']:
            images = getattr(req, "images", None) or ()
            content = [{"type": "input_text", "text": req.text}]
            for img in images: content.append({"type": "input_image", "image_url": self._imgtourl(img)})
            messages = messages_override or [{"role": "user", "content": content}]
            resp = client.responses.create(model=model, input=messages, **openai_cfg[api_family])
            text = self._extracttextfromresponseobj(resp)
            raw = resp.model_dump() if hasattr(resp, "model_dump") else resp
            return ChatResponse(text=text, raw=raw)
        else:
            raise TypeError(f"Unsupported api_family: {api_family}")
    '''send'''
    def send(self, req: Any, api: Optional[str] = None, version: Optional[str] = None, request_overrides: dict = None) -> ChatResponse:
        # set proxies
        if self.auto_set_proxies:
            try: self.session.proxies = self.proxied_session_client.getrandomproxy()
            except: self.session.proxies = {}
        # model version
        version = version or self.default_version
        if version not in self.variants: raise ValueError(f"Unknown version '{version}'. Available: {list(self.variants.keys())}")
        # variant
        variant, req_io = self.variants[version], self.inferio(req)
        # assert io
        if req_io not in variant.io_supported: raise ValueError(f"Variant {variant.id} does not support {req_io.detailedtag()}")
        # with specified api
        if api is not None:
            spec = variant.apis.get(api)
            if spec is None: raise ValueError(f"Unknown api '{api}'. Available: {list(variant.apis.keys())}")
            if spec.io != req_io: raise ValueError(f"API '{api}' does not support {req_io.detailedtag()}, supports {spec.io.detailedtag()}")
            out: ChatResponse = getattr(self, spec.handler)(req, request_overrides=request_overrides, version=version)
            return ChatResponse(text=out.text, raw=out.raw, api_used=spec.name, variant_used=variant.id)
        # without specified api, select the best one
        candidates = [s for s in variant.apis.values() if s.io == req_io]
        if not candidates: raise ValueError(f"No API supports {req_io.detailedtag()} in variant {variant.id}")
        best = max(candidates, key=lambda s: s.priority)
        out: ChatResponse = getattr(self, best.handler)(req, request_overrides=request_overrides, version=version)
        # return
        return ChatResponse(text=out.text, raw=out.raw, api_used=best.name, variant_used=variant.id)
    '''describe'''
    def describe(self) -> Dict[str, Any]:
        return {
            "provider": self.provider, "model": self.model, "default_version": self.default_version,
            "versions": {
                ver: {
                    "variant_id": v.id, "io_supported": [io.detailedtag() for io in v.io_supported],
                    "apis": {name: {"io": spec.io.detailedtag(), "priority": spec.priority, "note": spec.note, "handler": spec.handler} for name, spec in v.apis.items()},
                } for ver, v in self.variants.items()
            },
        }
    '''_extracttextfromresponseobj'''
    @staticmethod
    def _extracttextfromresponseobj(resp: Any) -> str:
        txt = getattr(resp, "output_text", None)
        if isinstance(txt, str) and txt.strip(): return txt.strip()
        out = getattr(resp, "output", None) or []
        texts: List[str] = []
        for item in out:
            if getattr(item, "type", None) != "message" or getattr(item, "role", None) != "assistant": continue
            for part in getattr(item, "content", None) or []:
                if getattr(part, "type", None) == "output_text":
                    t = getattr(part, "text", "")
                    if isinstance(t, str) and t.strip(): texts.append(t.strip())
        return "\n".join(texts).strip()
    '''_extracttextfromchatcompletionsobj'''
    @staticmethod
    def _extracttextfromchatcompletionsobj(resp: Any) -> str:
        choices, texts = resp.choices, []
        for item in choices:
            if not hasattr(item, 'message') or item.message.role not in ["assistant"]: continue
            texts.append(item.message.content)
        return "\n".join(texts).strip()
    '''_imgtourl'''
    @staticmethod
    def _imgtourl(img: Union[str, bytes, Tuple[bytes, str]]) -> str:
        if isinstance(img, str):
            s = img.strip()
            if s.startswith("http://") or s.startswith("https://") or s.startswith("data:"): return s
            raise ValueError("Image str must be http(s) URL or data: URL")
        if isinstance(img, tuple):
            b, mime = img
            b64 = base64.b64encode(b).decode("utf-8")
            return f"data:{mime};base64,{b64}"
        if isinstance(img, (bytes, bytearray)):
            b64 = base64.b64encode(bytes(img)).decode("utf-8")
            return f"data:image/png;base64,{b64}"
        raise TypeError(f"Unsupported image type: {type(img)}")


'''EndpointRegistry'''
class EndpointRegistry:
    def __init__(self):
        self._endpoints: List[BaseEndpoint] = []
    '''register'''
    def register(self, endpoint: BaseEndpoint):
        self._endpoints.append(endpoint)
    '''listall'''
    def listall(self) -> List[Dict[str, Any]]:
        return [ep.describe() for ep in self._endpoints]
    '''findvariantsbyio'''
    def findvariantsbyio(self, io: Union[str, ModelIOType]) -> List[Tuple[BaseEndpoint, str]]:
        target = ModelIOType.fromtag(io) if isinstance(io, str) else io
        hits: List[Tuple[BaseEndpoint, str]] = []
        for ep in self._endpoints:
            for ver, v in ep.variants.items():
                if target in v.io_supported: hits.append((ep, ver))
        return hits
    '''get'''
    def get(self, provider: str, model: str) -> List[BaseEndpoint]:
        return [ep for ep in self._endpoints if ep.provider == provider and ep.model == model]