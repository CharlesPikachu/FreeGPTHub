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
    def __init__(self, engine: AIEngine):
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
        return aslines(self.engine.run(prompt, system=_BASE_SYSTEM, temperature=0.6, max_tokens=300))
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
        return aslines(self.engine.run(prompt, system=_BASE_SYSTEM, temperature=0.4, max_tokens=280))
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
        return aslines(self.engine.run(prompt, system=_BASE_SYSTEM, temperature=0.5, max_tokens=160))
    '''pomodoroplan'''
    def pomodoroplan(self, drama_title: str, total_eps: int | None, eps: list, time_limit_min: int = 15) -> str:
        prompt = f"""
用户只有 {time_limit_min} 分钟摸鱼。给一个观看策略: 看哪些集最划算 (最多 3 集)。
严格输出格式:
策略: ...
清单:
1) 第X集 | 理由(<=12字)
2) 第X集 | 理由(<=12字)
3) 第X集 | 理由(<=12字)
提醒: 一句伪装成工作的提醒(<=16字)

剧名：{drama_title}
总集数(可空): {total_eps}
每集详情: {' | '.join([str(e) for e in eps])}
"""
        return aslines(self.engine.run(prompt, system=_BASE_SYSTEM, temperature=0.5, max_tokens=220))
    '''stealthtitles'''
    def stealthtitles(self, titles: List[str], style: str = "trainlog") -> List[str]:
        out: List[str] = []
        for i, _ in enumerate(titles, 1):
            if style == "trainlog": out.append(f"Epoch {i}/200 | loss=0.{(i*7)%100:02d} | val_auc=0.{(80+i)%100:02d} | step={(i*120)%9999}")
            elif style == "build": out.append(f"[build] target_{i} ✔ (0.{(i*13)%100:02d}s)")
            elif style == "docs": out.append(f"[doc] section_{i} updated ✔")
            else: out.append(f"[log] task_{i}: running...")
        return out
    '''bosskeymessage'''
    def bosskeymessage(self) -> str:
        return "(隐身中) 正在检查训练日志与系统状态... ✔"