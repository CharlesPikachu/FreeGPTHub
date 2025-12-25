'''
Function:
    Implementation of Models
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


'''Episode'''
@dataclass
class Episode:
    ep: int
    title: str = ""
    duration_sec: Optional[int] = None
    play_url: Optional[str] = None
    video_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


'''Drama'''
@dataclass
class Drama:
    id: str
    title: str
    desc: str = ""
    cover: str = ""
    author: str = ""
    tags: str = ""
    total_eps: Optional[int] = None
    episodes: List[Episode] = field(default_factory=list)
    engine: str = "HongGuoProvider"
    extra: Dict[str, Any] = field(default_factory=dict)