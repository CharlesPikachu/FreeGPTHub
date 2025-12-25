'''
Function:
    Implementation of AI Engine Related Functions
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import time
from dataclasses import dataclass
from freegpthub import MiniMaxEndpoints, ChatRequest
from typing import Any, Dict, List, Optional, Protocol


'''AIContext'''
@dataclass
class AIContext:
    user_text: str
    recent_queries: List[str]
    recent_events: List[Dict[str, Any]]
    candidates: List[Dict[str, Any]]
    likes: Dict[str, int]
    dislikes: Dict[str, int]


'''LLM'''
class LLM(Protocol):
    def complete(self, prompt: str, system: str | None = None, temperature: float = 0.6, max_tokens: int = 600, **kwargs: Any,) -> str: ...


'''FreeGPTHubLLM'''
class FreeGPTHubLLM:
    def __init__(self, aes_gem_key: Optional[str] = None, retries: int = 2, retry_backoff_sec: float = 1.2):
        self.version = 'MiniMax-M2'
        self.aes_gem_key = aes_gem_key
        self.retries = max(0, int(retries))
        self.retry_backoff_sec = float(retry_backoff_sec)
        self.client = MiniMaxEndpoints(aes_gem_key=aes_gem_key)
    '''complete'''
    def complete(self, prompt: str, system: str | None = None, temperature: float = 0.6, **kwargs: Any) -> str:
        messages: List[Dict[str, str]] = []
        if system: messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        openai_cfg: Dict[str, Any] = {"client.chat.completions.create": {"messages": messages, "temperature": temperature}, "client": {}}
        openai_cfg.update(kwargs)
        req = ChatRequest(text=prompt, openai=openai_cfg)
        last_err: Optional[Exception] = None
        resp = self.client.send(req=req, version=self.version)
        for i in range(self.retries + 1):
            try:
                resp = self.client.send(req=req, version=self.version)
                return (resp.text or "").strip()
            except Exception as e:
                last_err = e
                if i >= self.retries: break
                time.sleep(self.retry_backoff_sec * (i + 1))
        raise RuntimeError(f"FreeGPTHub call failed after retries. last_error={last_err}") from last_err


'''AIEngine'''
class AIEngine:
    def __init__(self, llm: LLM, default_system: str = ""):
        self.llm = llm
        self.default_system = default_system.strip()
    '''run'''
    def run(self, prompt: str, system: str | None = None, temperature: float = 0.6, max_tokens: int = 2048, **kwargs: Any) -> str:
        sys = (system if system is not None else self.default_system) or None
        return self.llm.complete(
            prompt=prompt, system=sys, temperature=temperature, max_tokens=max_tokens, **kwargs,
        )