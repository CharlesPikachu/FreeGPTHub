'''
Function:
    Implementation of BaseProvider
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import requests
from typing import List, Protocol
from ..utils import Drama, Episode
from typing import Any, Dict, List, Optional


'''Provider'''
class Provider(Protocol):
    source: str
    api_urls: list
    def search(self, query: str, page: int = 1) -> List[Drama]: ...
    def listepisodes(self, drama: Drama) -> List[Episode]: ...
    def getplayurl(self, drama: Drama, ep: Episode) -> str: ...


'''BaseProvider'''
class BaseProvider():
    source, api_urls = 'BaseProvider', []
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        raise NotImplementedError
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        raise NotImplementedError
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        raise NotImplementedError
    '''saferequestsget'''
    def saferequestsget(self, params: Dict[str, Any], requests_overrides: dict = None):
        requests_overrides, raw = requests_overrides or {}, {}
        for api_url in self.api_urls:
            try:
                resp = self.session.get(api_url, params=params, timeout=15, **requests_overrides)
                resp.raise_for_status()
                raw = resp.json()
                if isinstance(raw, dict) and raw.get("code") not in (None, 200): raise RuntimeError(raw.get('msg'))
                break
            except:
                continue
        return raw
    '''safeint'''
    def safeint(self, x: Any) -> Optional[int]:
        try:
            if x is None: return None
            return int(float(x))
        except Exception:
            return None