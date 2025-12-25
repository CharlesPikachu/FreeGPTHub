'''
Function:
    Implementation of Client Functions
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import os
import re
import locale
import argparse
from rich.table import Table
from rich import print as rprint
from typing import Any, Dict, List, Optional
try:
    from modules import PklStore, Drama, Episode, ProviderBulder, AIServices, AIEngine, FreeGPTHubLLM, AIContext, Provider, mpvplayplaylist, mpvplayurl
except:
    from .modules import PklStore, Drama, Episode, ProviderBulder, AIServices, AIEngine, FreeGPTHubLLM, AIContext, Provider, mpvplayplaylist, mpvplayurl


'''settings'''
DEFAULT_ENGINE = "HongGuoProvider"
LANGUAGE = ["zh", "en"][0]


'''showdramas'''
def showdramas(dramas: List[Dict[str, Any]]) -> None:
    if not dramas: rprint("No short-drama information available to display") if LANGUAGE == 'en' else rprint('没有短剧信息可以打印'); return
    if LANGUAGE == 'zh':
        table = Table(title="搜索结果 (剧)")
        table.add_column("#", justify="right")
        table.add_column("标题")
        table.add_column("引擎")
        table.add_column("集数")
        table.add_column("标签/类型")
    else:
        table = Table(title="Search Results (Drama)")
        table.add_column("#", justify="right")
        table.add_column("Title")
        table.add_column('Engine')
        table.add_column('Episodes')
        table.add_column('Tags')
    for drama_idx, drama in enumerate(dramas, 1):
        table.add_row(str(drama_idx), str(drama.get("title", "")), str(drama.get("engine", "")), str(drama.get("total_eps", "") or ""), str(drama.get("tags", "") or ""))
    rprint(table)


'''showepisodes'''
def showepisodes(episodes: List[Dict[str, Any]], progress: int = 0) -> None:
    if not episodes: rprint("Failed to retrieve the episode list") if LANGUAGE == 'en' else rprint('未获取到集列表'); return
    if LANGUAGE == 'zh':
        table = Table(title=f"集列表 (已看到: 第{progress}集)" if progress else "集列表")
        table.add_column("集", justify="right")
        table.add_column("标题")
        table.add_column("时长 (s)")
        table.add_column("有播放链接")
    else:
        table = Table(f"Episode List (Watched up to: Episode {progress})" if progress else "Episode List")
        table.add_column("Episode", justify="right")
        table.add_column("Title")
        table.add_column("Duration (s)")
        table.add_column("Playable")
    for episode in episodes:
        ok = "Y" if episode.get("play_url") else ""
        table.add_row(str(episode.get("ep")), str(episode.get("title", "")), str(episode.get("duration_sec") or ""), ok)
    rprint(table)


'''dramafromlight'''
def dramafromlight(d: Dict[str, Any]) -> Drama:
    return Drama(
        id=str(d["id"]), title=str(d.get("title", "")), desc=str(d.get("desc", "")), cover=str(d.get("cover", "")), tags=str(d.get("tags", "")),
        total_eps=(int(d["total_eps"]) if d.get("total_eps") not in (None, "") else None), engine=str(d.get("engine", "HongGuoProvider")), extra=d.get("extra") or {},
    )


'''episodefromlight'''
def episodefromlight(e: Dict[str, Any]) -> Episode:
    return Episode(
        ep=int(e["ep"]), title=str(e.get("title", "")), duration_sec=(int(e["duration_sec"]) if e.get("duration_sec") not in (None, "") else None),
        play_url=e.get("play_url"), video_id=e.get("video_id"), extra=e.get("extra") or {},
    )


'''cmdsearch'''
def cmdsearch(args: argparse.Namespace, store: PklStore) -> int:
    provider: Provider = ProviderBulder.REGISTERED_MODULES[args.engine]()
    dramas = provider.search(args.query, page=args.page)
    light: List[Dict[str, Any]] = []
    for drama in dramas:
        light.append({
            "id": drama.id, "title": drama.title, "desc": drama.desc, "cover": drama.cover, "author": drama.author, "tags": drama.tags,
            "total_eps": drama.total_eps, "engine": drama.engine, "extra": drama.extra,
        })
    store.setlastdramas(args.query, light)
    showdramas(light)
    return 0


'''cmdepisodes'''
def cmdepisodes(args: argparse.Namespace, store: PklStore) -> int:
    dramas = store.getlastdramas()
    if not dramas: rprint('No recent search results, please run "search" first') if LANGUAGE == 'en' else rprint('没有最近搜索结果, 请先 "search"'); return 1
    idx = ((args.idx - 1) if args.idx > 0 else args.idx) % (len(dramas))
    drama = dramas[idx]
    drama = dramafromlight(drama)
    provider: Provider = ProviderBulder.REGISTERED_MODULES[drama.engine]()
    cached = store.getcachedepisodes(drama.id)
    if cached and not args.refresh:
        eps_light = cached
    else:
        episodes, eps_light = provider.listepisodes(drama), []
        for episode in episodes:
            eps_light.append({
                "ep": episode.ep, "title": episode.title, "duration_sec": episode.duration_sec, "play_url": episode.play_url,
                "video_id": episode.video_id, "extra": episode.extra,
            })
        store.cacheepisodes(drama.id, eps_light)
    prog = store.getprogress(drama.id)
    showepisodes(eps_light, progress=prog)
    return 0


'''ensureepisodes'''
def ensureepisodes(store: PklStore, drama: Drama, provider: Provider) -> List[Dict[str, Any]]:
    eps_light = store.getcachedepisodes(drama.id)
    if eps_light: return eps_light
    episodes, eps_light = provider.listepisodes(drama), []
    for episode in episodes:
        eps_light.append({
            "ep": episode.ep, "title": episode.title, "duration_sec": episode.duration_sec, "play_url": episode.play_url,
            "video_id": episode.video_id, "extra": episode.extra,
        })
    store.cacheepisodes(drama.id, eps_light)
    return eps_light


'''cmdplay'''
def cmdplay(args: argparse.Namespace, store: PklStore) -> int:
    dramas = store.getlastdramas()
    if not dramas: rprint('No recent search results, please run "search" first') if LANGUAGE == 'en' else rprint('没有最近搜索结果, 请先 "search"'); return 1
    idx = ((args.idx - 1) if args.idx > 0 else args.idx) % (len(dramas))
    drama = dramas[idx]
    drama = dramafromlight(dramas[idx])
    provider: Provider = ProviderBulder.REGISTERED_MODULES[drama.engine]()
    eps_light, target_ep = ensureepisodes(store, drama, provider), None
    for e in eps_light:
        if int(e["ep"]) == args.ep: target_ep = e; break
    if not target_ep: rprint('Episode not found, please run "eps" first to check the available episode numbers') if LANGUAGE == 'en' else rprint('未找到该集, 请先 "eps" 查看集号'); return 1
    ep = episodefromlight(target_ep)
    url = provider.getplayurl(drama, ep)
    rc = mpvplayurl(url, vo=args.vo)
    if rc == 0: store.setprogress(drama.id, ep.ep)
    return rc


'''cmdresume'''
def cmdresume(args: argparse.Namespace, store: PklStore) -> int:
    dramas = store.getlastdramas()
    if not dramas: rprint('No recent search results, please run "search" first') if LANGUAGE == 'en' else rprint('没有最近搜索结果, 请先 "search"'); return 1
    idx = ((args.idx - 1) if args.idx > 0 else args.idx) % (len(dramas))
    drama = dramafromlight(dramas[idx])
    provider: Provider = ProviderBulder.REGISTERED_MODULES[drama.engine]()
    ensureepisodes(store, drama, provider)
    last = store.getprogress(drama.id)
    next_ep = last + 1 if last >= 1 else 1
    if drama.total_eps and next_ep > drama.total_eps: rprint(f"Finished already? (last recorded: Episode {last}; total episodes: {drama.total_eps})") if LANGUAGE == 'en' else rprint(f"已看完? (记录到第 {last} 集, 总集数 {drama.total_eps})"); return 0
    args.ep = next_ep
    return cmdplay(args, store)


'''cmdbinge'''
def cmdbinge(args: argparse.Namespace, store: PklStore) -> int:
    dramas = store.getlastdramas()
    if not dramas: rprint('No recent search results, please run "search" first') if LANGUAGE == 'en' else rprint('没有最近搜索结果, 请先 "search"'); return 1
    idx = ((args.idx - 1) if args.idx > 0 else args.idx) % (len(dramas))
    drama = dramafromlight(dramas[idx])
    provider: Provider = ProviderBulder.REGISTERED_MODULES[drama.engine]()
    eps_light = ensureepisodes(store, drama, provider)
    urls: List[str] = []
    to_ep = args.to
    if drama.total_eps and to_ep > drama.total_eps: to_ep = drama.total_eps
    for epno in range(args.from_ep, to_ep + 1):
        target = None
        for e in eps_light:
            if int(e["ep"]) == epno: target = e; break
        if not target: continue
        ep = episodefromlight(target)
        try:
            url = provider.getplayurl(drama, ep)
            urls.append(url)
        except Exception as ex:
            rprint(f"Failed to parse Episode {epno}: {ex}" if LANGUAGE == 'en' else f"第{epno}集解析失败: {ex}")
            break
    if not urls: rprint("No playable link available") if LANGUAGE == 'en' else rprint("没有可播放的链接"); return 1
    rc = mpvplayplaylist(urls, vo=args.vo)
    if rc == 0: store.setprogress(drama.id, to_ep)
    return rc


'''aictx'''
def aictx(store: PklStore, user_text: str = "", candidates: Optional[List[Dict[str, Any]]] = None) -> AIContext:
    return AIContext(
        user_text=user_text, recent_queries=store.state.recent_queries, recent_events=[], candidates=candidates or store.getlastdramas(),
        likes=store.state.likes, dislikes=store.state.dislikes,
    )


'''cmdaisuggest'''
def cmdaisuggest(args: argparse.Namespace, store: PklStore, aes_gem_key: bytes) -> int:
    engine = AIEngine(FreeGPTHubLLM(aes_gem_key=aes_gem_key))
    svc = AIServices(engine)
    ctx = aictx(store)
    out = svc.suggestkeywords(ctx, mood=args.mood or "", avoid=args.avoid or "", n=args.n)
    rprint(out)
    return 0


'''cmdairewrite'''
def cmdairewrite(args: argparse.Namespace, store: PklStore, aes_gem_key: bytes) -> int:
    engine = AIEngine(FreeGPTHubLLM(aes_gem_key=aes_gem_key))
    svc = AIServices(engine)
    ctx = aictx(store, user_text=args.text)
    out = svc.rewritequery(ctx)
    rprint(out)
    return 0


'''cmdaihook'''
def cmdaihook(args: argparse.Namespace, store: PklStore, aes_gem_key: bytes) -> int:
    dramas = store.getlastdramas()
    if not dramas: rprint('No recent search results, please run "search" first') if LANGUAGE == 'en' else rprint('没有最近搜索结果, 请先 "search"'); return 1
    idx = ((args.idx - 1) if args.idx > 0 else args.idx) % (len(dramas))
    drama = dramafromlight(dramas[idx])
    provider: Provider = ProviderBulder.REGISTERED_MODULES[drama.engine]()
    eps_light = ensureepisodes(store, drama, provider)
    engine = AIEngine(FreeGPTHubLLM(aes_gem_key=aes_gem_key))
    svc = AIServices(engine)
    out = svc.hookepisode(drama.title, drama.total_eps, eps_light)
    rprint(out)
    return 0


'''detectlangfromsystemlocale'''
def detectlangfromsystemlocale() -> str:
    try: locale.setlocale(locale.LC_ALL, "")
    except locale.Error: pass
    candidates = []
    try:
        msg_loc = locale.getlocale(locale.LC_MESSAGES)
        if msg_loc and msg_loc[0]: candidates.append(msg_loc[0])
    except Exception:
        pass
    try:
        loc = locale.getlocale()
        if loc and loc[0]: candidates.append(loc[0])
    except Exception:
        pass
    for k in ("LC_ALL", "LC_MESSAGES", "LANG"):
        v = os.environ.get(k)
        if v: candidates.append(v)
    s = " ".join(candidates).lower()
    if re.search(r"\bzh\b|zh[_-](cn|sg|hk|tw|hans|hant)", s) or "chinese" in s: return "zh"
    return "en"


'''buildparser'''
def buildparser() -> argparse.ArgumentParser:
    # decide language
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--lang", choices=["zh", "en", "auto"], default="auto")
    ns, _ = pre.parse_known_args()
    if ns.lang == "auto": lang = detectlangfromsystemlocale()
    else: lang = ns.lang
    LANGUAGE = lang
    # translate table
    I18N = {
        "desc": {
            "zh": "终端摸鱼看短剧: 多集播放 + 可选搜索引擎 + AI 搜索助手",
            "en": "Terminal short-drama bingeing (for sneaky breaks): multi-episode playback + selectable search engines + AI-powered search assistant",
        },
        "engine": {
            "zh": "搜索引擎 (默认: HongGuoProvider)", "en": "Search engine (Default: HongGuoProvider)",
        },
        "state": {
            "zh": "pkl 状态文件路径 (默认: ~/.drama_moyu_state.pkl)", "en": "Path to pkl state file (Default: ~/.drama_moyu_state.pkl)",
        },
        "search_help": {"zh": "搜索短剧 (剧层级)", "en": "Search dramas (series-level)"},
        "eps_help": {"zh": "获取某部剧的集列表 (基于最近搜索结果 idx)", "en": "List episodes (by idx from latest search)"},
        "play_help": {"zh": "播放某部剧的某一集 (基于最近搜索结果 idx)", "en": "Play an episode (by idx from latest search)"},
        "resume_help": {"zh": "续播: 播放上次记录的下一集", "en": "Resume: play next episode from last record"},
        "binge_help": {"zh": "连播: 播放一段集数区间", "en": "Binge: play a range of episodes"},
        "ai_help": {"zh": "AI 功能 (FreeGPTHub + GLM4.5)", "en": "AI tools (FreeGPTHub + GLM4.5)"},
        "suggest_help": {"zh": "AI: 根据历史搜索给关键词建议", "en": "AI: suggest keywords from your search history"},
        "rewrite_help": {"zh": "AI: 把口语需求改写为更好搜的关键词", "en": "AI: rewrite casual request into better search keywords"},
        "hook_help": {"zh": "AI: 给某部剧入坑集建议 (idx 来自最近搜索结果)", "en": "AI: recommend a good starting episode (idx from latest search)"},
    }
    def T(k: str) -> str: return I18N.get(k, {}).get(LANGUAGE, k)
    # parser
    p = argparse.ArgumentParser(prog="drama_moyu", parents=[pre], description=T("desc"))
    # --root
    p.add_argument("--engine", default=DEFAULT_ENGINE, choices=list(ProviderBulder.REGISTERED_MODULES.keys()), help=T("engine"))
    p.add_argument("--state", default=None, help=T("state"))
    sp = p.add_subparsers(dest="cmd", required=True)
    # --search
    s = sp.add_parser("search", help=T("search_help"))
    s.add_argument("query")
    s.add_argument("--page", type=int, default=1)
    s.set_defaults(fn=cmdsearch)
    # --eps
    e = sp.add_parser("eps", help=T("eps_help"))
    e.add_argument("idx", type=int)
    e.add_argument("--refresh", action="store_true")
    e.set_defaults(fn=cmdepisodes)
    # --player
    pl = sp.add_parser("play", help=T("play_help"))
    pl.add_argument("idx", type=int)
    pl.add_argument("--ep", type=int, required=True)
    pl.add_argument("--vo", default=None, help="mpv vo (e.g., tct/caca / leave empty for default)" if LANGUAGE == "en" else "mpv vo（如 tct/caca/默认不填）")
    pl.set_defaults(fn=cmdplay)
    # --resume
    rs = sp.add_parser("resume", help=T("resume_help"))
    rs.add_argument("idx", type=int)
    rs.add_argument("--vo", default=None)
    rs.set_defaults(fn=cmdresume)
    # --binge
    bg = sp.add_parser("binge", help=T("binge_help"))
    bg.add_argument("idx", type=int)
    bg.add_argument("--from", dest="from_ep", type=int, default=1)
    bg.add_argument("--to", dest="to", type=int, default=10)
    bg.add_argument("--vo", default=None)
    bg.set_defaults(fn=cmdbinge)
    # --ai
    ai = sp.add_parser("ai", help=T("ai_help"))
    ai_sp = ai.add_subparsers(dest="ai_cmd", required=True)
    a1 = ai_sp.add_parser("suggest", help=T("suggest_help"))
    a1.add_argument("--mood", default="")
    a1.add_argument("--avoid", default="")
    a1.add_argument("-n", type=int, default=8)
    a1.set_defaults(fn=cmdaisuggest)
    a2 = ai_sp.add_parser("rewrite", help=T("rewrite_help"))
    a2.add_argument("text")
    a2.set_defaults(fn=cmdairewrite)
    a3 = ai_sp.add_parser("hook", help=T("hook_help"))
    a3.add_argument("idx", type=int)
    a3.set_defaults(fn=cmdaihook)
    # return
    return p


'''main'''
def main(argv: Optional[List[str]] = None) -> int:
    parser = buildparser()
    args = parser.parse_args(argv)
    store = PklStore(path=args.state) if args.state else PklStore()
    return args.fn(args, store)


'''tests'''
if __name__ == '__main__': main()