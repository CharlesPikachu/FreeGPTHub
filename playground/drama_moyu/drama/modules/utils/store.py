'''
Function:
    Implementation of Storage Related Functions
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import os
import pickle
from typing import Any, Dict, List
from dataclasses import dataclass, field


'''settings'''
DEFAULT_PATH = os.path.expanduser("~/.drama_moyu_state.pkl")


'''AppState'''
@dataclass
class AppState:
    last_query: str = ""
    last_dramas: List[Dict[str, Any]] = field(default_factory=list)
    episodes_cache: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    progress: Dict[str, int] = field(default_factory=dict)
    likes: Dict[str, int] = field(default_factory=dict)
    dislikes: Dict[str, int] = field(default_factory=dict)
    recent_queries: List[str] = field(default_factory=list)


'''PklStore'''
class PklStore:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.state = self._load()
    '''_load'''
    def _load(self) -> AppState:
        if not os.path.exists(self.path): return AppState()
        try:
            with open(self.path, "rb") as f: obj = pickle.load(f)
            if isinstance(obj, AppState): return obj
            if isinstance(obj, dict):
                st = AppState()
                for k, v in obj.items():
                    if hasattr(st, k): setattr(st, k, v)
                return st
            return AppState()
        except Exception:
            return AppState()
    '''save'''
    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "wb") as f: pickle.dump(self.state, f)
    '''setlastdramas'''
    def setlastdramas(self, query: str, dramas_light: List[dict]) -> None:
        self.state.last_query = query
        self.state.last_dramas = dramas_light
        if query.strip(): self.state.recent_queries = ([query.strip()] + self.state.recent_queries)[:50]
        self.save()
    '''getlastdramas'''
    def getlastdramas(self) -> List[dict]:
        return self.state.last_dramas or []
    '''cacheepisodes'''
    def cacheepisodes(self, drama_id: str, eps_light: List[dict]) -> None:
        self.state.episodes_cache[drama_id] = eps_light
        self.save()
    '''getcachedepisodes'''
    def getcachedepisodes(self, drama_id: str) -> List[dict]:
        return self.state.episodes_cache.get(drama_id, [])
    '''setprogress'''
    def setprogress(self, drama_id: str, ep: int) -> None:
        self.state.progress[drama_id] = int(ep)
        self.save()
    '''getprogress'''
    def getprogress(self, drama_id: str) -> int:
        return int(self.state.progress.get(drama_id, 0))