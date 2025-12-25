'''
Function:
    Implementation of AI Plugins Related Functions
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import re
from typing import Any, Dict, List
from .engine import AIContext, AIEngine


'''settings'''
_BASE_SYSTEM = """你是一个“短剧摸鱼助手”, 专门帮用户生成可直接用于搜索短剧的关键词组合, 并能做需求改写、去重、限时观看计划、入坑集推荐等。
要求:
- 输出要短、可复制粘贴、可直接用于搜索;
- 不要输出长段解释;
- 如需结构化输出，严格遵守用户要求的格式;
- 默认中文输出。
"""
_BASE_SYSTEM_EN = """You are a "Short-Drama Slack-Off Assistant", specialized in helping users generate keyword combinations that can be directly used to search for short dramas, and can also handle request rewriting, deduplication, time-limited watching plans, and entry-episode recommendations, etc.
Requirements:
- The output should be short, copyable, and directly usable for search;
- Do not output long explanatory paragraphs;
- If structured output is needed, strictly follow the user-required format;
- Default output in English.
"""


'''aslines'''
def aslines(text: str) -> str:
    return "\n".join([ln.rstrip() for ln in text.strip().splitlines() if ln.strip()])


'''localtitlenorm'''
def localtitlenorm(t: str) -> str:
    x = re.sub(r"\s+", "", t)
    x = re.sub(r"[【】\[\]（）()《》:：\-—_]", "", x)
    x = re.sub(r"\d{1,3}集.*?$", "", x)
    return x.lower()


'''AIServices'''
class AIServices:
    def __init__(self, engine: AIEngine, lang: str = 'zh'):
        self.lang = lang
        self.engine = engine
    '''suggestkeywords'''
    def suggestkeywords(self, ctx: AIContext, mood: str = "", avoid: str = "", n: int = 8) -> str:
        prompt = f"""
根据用户偏好与历史搜索, 生成 {n} 条“短剧搜索关键词串” (每行一条), 每条建议包含:
题材/关系 + 人设标签 + 情绪/节奏 + 爽点关键词 (如 复仇/逆袭/甜宠/高能反转/爽文/追妻火葬场 等)。
约束:
- 每条不超过 18 个汉字 (含空格也算);
- 不要编号, 不要解释, 不要标点堆叠;
- 必须避开用户雷点。

用户心情(可空): {mood}
需要避开(可空): {avoid}

喜欢标签计数: {ctx.likes}
不喜欢标签计数: {ctx.dislikes}

最近搜索(最多12条): {ctx.recent_queries[:12]}
"""
        prompt_en = f"""
Based on the user's preferences and search history, generate {n} "short-drama search keyword strings" (one per line). Each suggestion should include:
Genre/relationship + character archetype tags + emotion/pacing + "feel-good" hook keywords (e.g., revenge / comeback / sweet romance / high-energy twists / power fantasy / chasing-wife-crematorium, etc.).
Constraints:
- Each line must be no more than 18 Chinese characters (spaces count);
- No numbering, no explanations, no excessive punctuation;
- Must avoid the user's deal-breakers.

User mood (optional): {mood}
To avoid (optional): {avoid}

Liked tag counts: {ctx.likes}
Disliked tag counts: {ctx.dislikes}

Recent searches (up to 12): {ctx.recent_queries[:12]}
"""
        return aslines(self.engine.run(prompt if self.lang == 'zh' else prompt_en, system=_BASE_SYSTEM if self.lang == 'zh' else _BASE_SYSTEM_EN, temperature=0.6))
    '''rewritequery'''
    def rewritequery(self, ctx: AIContext) -> str:
        prompt = f"""
把用户口语需求改写成更好搜的短剧关键词。
严格输出以下格式 (每行一个字段，字段名不要改):
主查询: ...
备选1: ...
备选2: ...
备选3: ...
过滤: ... (没有就写 空)

用户需求: {ctx.user_text}

最近搜索参考(最多10条): {ctx.recent_queries[:10]}
"""
        prompt_en = f"""
Rewrite the user's casual request into short-drama keywords that are easier to search.
Strictly output the following format (one field per line; do not change the field names):
Main query: ...
Alternative 1: ...
Alternative 2: ...
Alternative 3: ...
Filter: ... (write Empty if none)

User request: {ctx.user_text}

Recent search references (up to 10): {ctx.recent_queries[:10]}
"""
        return aslines(self.engine.run(prompt if self.lang == 'zh' else prompt_en, system=_BASE_SYSTEM if self.lang == 'zh' else _BASE_SYSTEM_EN, temperature=0.4))
    '''dedupdramas'''
    def dedupdramas(self, dramas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        groups: Dict[str, List[Dict[str, Any]]] = {}
        for d in dramas:
            key = localtitlenorm(str(d.get("title", "")))
            if not key: key = d.get("id", "")
            groups.setdefault(key, []).append(d)
        return [v[0] for v in groups.values()]
    '''hookepisode'''
    def hookepisode(self, drama_title: str, total_eps: int | None, eps: list) -> str:
        prompt = f"""
给这部短剧一个“入坑集”建议: 从第几集开始最容易上头? 给出 1 个主建议和 2 个备选。
严格输出格式:
主入坑: 第X集 | 一句理由(<=12字)
备选1: 第X集 | 一句理由(<=12字)
备选2: 第X集 | 一句理由(<=12字)

剧名：{drama_title}
总集数(可空): {total_eps}
每集详情: {' | '.join([str(e) for e in eps])}
"""
        prompt_en = f"""
Give an "entry episode" suggestion for this short drama: which episode is the easiest to get hooked from? Provide 1 main suggestion and 2 alternatives.
Strict output format:
Main entry: Episode X | One-line reason (<=12 chars)
Alt 1: Episode X | One-line reason (<=12 chars)
Alt 2: Episode X | One-line reason (<=12 chars)

Title: {drama_title}
Total episodes (optional): {total_eps}
Episode details: {' | '.join([str(e) for e in eps])}
"""
        return aslines(self.engine.run(prompt if self.lang == 'zh' else prompt_en, system=_BASE_SYSTEM if self.lang == 'zh' else _BASE_SYSTEM_EN, temperature=0.5))