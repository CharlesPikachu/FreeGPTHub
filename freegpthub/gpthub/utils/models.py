'''
Function:
    Implementation of Data Models
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, Iterable, Optional, Tuple, Union


'''ModelIOType'''
@dataclass(frozen=True, slots=True)
class ModelIOType:
    class Modality(Enum):
        TEXT, IMAGE, AUDIO, VIDEO = "text", "image", "audio", "video"
        @property
        def short(self) -> str:
            return {self.TEXT: "T", self.IMAGE: "I", self.AUDIO: "A", self.VIDEO: "V"}[self]
        @classmethod
        def fromany(cls, x: Union["ModelIOType.Modality", str]) -> "ModelIOType.Modality":
            if isinstance(x, cls): return x
            if not isinstance(x, str): raise TypeError(f"Unsupported modality type: {type(x)}")
            s = x.strip().lower()
            alias = {
                "t": "text", "text": "text", "txt": "text", "i": "image", "img": "image", "image": "image",
                "a": "audio", "aud": "audio", "audio": "audio", "v": "video", "vid": "video", "video": "video",
            }
            if s not in alias: raise ValueError(f"Unknown modality string: {x!r}")
            return cls(alias[s])
    inputs: FrozenSet[Modality]
    outputs: FrozenSet[Modality]
    name: Optional[str] = field(default=None, compare=False)
    meta: FrozenSet[str] = field(default_factory=frozenset, compare=False)
    @property
    def is_multimodal_input(self) -> bool:
        return len(self.inputs) > 1
    @property
    def is_multimodal_output(self) -> bool:
        return len(self.outputs) > 1
    @property
    def tag(self) -> str:
        def side(mods: FrozenSet[ModelIOType.Modality]) -> str:
            if len(mods) == 1: return next(iter(mods)).short
            return "MM"
        return f"{side(self.inputs)}2{side(self.outputs)}"
    '''postinit'''
    def __post_init__(self):
        if not self.inputs: raise ValueError("inputs cannot be empty")
        if not self.outputs: raise ValueError("outputs cannot be empty")
    '''tofrozenset'''
    @staticmethod
    def tofrozenset(mods: Iterable[Union["ModelIOType.Modality", str]]) -> FrozenSet["ModelIOType.Modality"]:
        return frozenset(ModelIOType.Modality.fromany(m) for m in mods)
    '''create'''
    @classmethod
    def create(cls, inputs: Iterable[Union["ModelIOType.Modality", str]], outputs: Iterable[Union["ModelIOType.Modality", str]], *, name: Optional[str] = None, meta: Optional[Iterable[str]] = None) -> "ModelIOType":
        return cls(inputs=cls.tofrozenset(inputs), outputs=cls.tofrozenset(outputs), name=name, meta=frozenset(meta or ()))
    '''detailedtag'''
    def detailedtag(self) -> str:
        def side(mods: FrozenSet[ModelIOType.Modality]) -> str:
            return "".join(sorted((m.short for m in mods)))
        return f"{side(self.inputs)}2{side(self.outputs)}"
    '''fromtag'''
    @classmethod
    def fromtag(cls, tag: str, *, name: Optional[str] = None) -> "ModelIOType":
        s = tag.strip().upper().replace(" ", "")
        if "2" not in s: raise ValueError(f"Invalid tag: {tag!r}")
        left, right = s.split("2", 1)
        if left == "MM" or right == "MM": raise ValueError("Cannot parse 'MM' tag because it does not specify exact modalities. Use create(inputs=..., outputs=...) instead.")
        short2mod = {"T": cls.Modality.TEXT, "I": cls.Modality.IMAGE, "A": cls.Modality.AUDIO, "V": cls.Modality.VIDEO}
        def _parseside(side: str) -> FrozenSet[ModelIOType.Modality]:
            if not side: raise ValueError(f"Empty side in tag: {tag!r}")
            mods = []
            for ch in side:
                if ch not in short2mod: raise ValueError(f"Unknown modality short '{ch}' in tag: {tag!r}")
                mods.append(short2mod[ch])
            return frozenset(mods)
        return cls(inputs=_parseside(left), outputs=_parseside(right), name=name)
    '''str'''
    def __str__(self) -> str:
        n = f"{self.name}: " if self.name else ""
        return f"{n}{self.detailedtag()} (canonical={self.tag})"


'''Modality'''
Modality = ModelIOType.Modality


'''ChatRequest'''
@dataclass(slots=True)
class ChatRequest:
    text: str = ""
    images: Tuple[Any, ...] = ()
    openai: Dict[str, Any] = field(default_factory=lambda: dict({'client': {}, 'client.responses.create': {}, 'client.chat.completions.create': {}}))
    websocket: Dict[str, Any] = field(default_factory=lambda: dict({'client': {}}))
    extra_payload: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)


'''ChatResponse'''
@dataclass(slots=True)
class ChatResponse:
    text: str
    raw: Any = None
    api_used: str = ""
    variant_used: str = ""


'''APISpec'''
@dataclass(frozen=True, slots=True)
class APISpec:
    name: str
    io: ModelIOType
    handler: str
    priority: int = 0
    note: str = ""


'''ModelVariant'''
@dataclass(slots=True)
class ModelVariant:
    provider: str
    model: str
    version: str
    io_supported: FrozenSet[ModelIOType]
    apis: Dict[str, APISpec] = field(default_factory=dict)
    @property
    def id(self) -> str:
        return f"{self.provider}:{self.model}:{self.version}"