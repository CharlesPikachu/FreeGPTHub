'''
Function:
    Implementation of HongGuoProvider
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import re
from tqdm import tqdm
from typing import List
from .base import BaseProvider
from ..utils import Drama, Episode


'''HongGuoProvider'''
class HongGuoProvider(BaseProvider):
    source = 'HongGuoProvider'
    api_urls = [
        "https://api-v2.cenguigui.cn/api/duanju/api.php", "https://api-v1.cenguigui.cn/api/duanju/api.php",
        "https://api.cenguigui.cn/api/duanju/api.php", "https://player.cenguigui.cn/api/duanju/api.php"
    ]
    def __init__(self):
        super(HongGuoProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={"name": query, "page": page})['data']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['book_id'], title=search_result['title'], desc=search_result['intro'], cover=search_result['cover'], tags=search_result['type'], 
                    engine=self.source, extra=search_result, author=search_result['author'], total_eps=search_result['episode_cnt'],
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={"book_id": drama.id})
        drama.title = drama_details.get('book_name') or drama.title
        drama.desc = drama_details.get('desc') or drama.desc
        drama.cover = drama_details.get('book_pic') or drama.cover
        drama.tags = ", ".join(drama_details.get('category_names')) or drama.tags
        drama.author = drama_details.get('author') or drama.author
        drama.total_eps = self.safeint(drama_details.get("total")) or drama.total_eps
        # iter to fetch
        play_list: list[dict] = drama_details.get("data") or []
        eps: List[Episode] = []
        cn_time_pat = re.compile(r'^\s*(?:(\d+)\s*(?:小时|时)\s*)?(?:(\d+)\s*分\s*)?(?:(\d+)\s*秒\s*)?\s*$')
        def to_sec(s: str) -> int:
            m = cn_time_pat.match(s)
            if not m: raise ValueError(f"bad time format: {s!r}")
            h, mi, se = (int(x) if x else 0 for x in m.groups())
            return h * 3600 + mi * 60 + se
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            ep_details: dict = self.saferequestsget(params={"video_id": it['video_id']})['data']
            it['ep_details'] = ep_details
            sort = re.search(r'第\s*(\d+)\s*集', it.get('title', ""))
            epno = self.safeint(sort.group(1)) if sort is not None else (i + 1)
            eps.append(Episode(
                ep=epno, title=str(it.get("title", "") or f"第{epno}集"), duration_sec=to_sec(ep_details['info'].get("duration")), play_url=ep_details.get("url"),
                video_id=it['video_id'], extra=it,
            ))
        # return
        drama.total_eps = (len(eps) if eps else None) or drama.total_eps
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        cn_time_pat = re.compile(r'^\s*(?:(\d+)\s*(?:小时|时)\s*)?(?:(\d+)\s*分\s*)?(?:(\d+)\s*秒\s*)?\s*$')
        def to_sec(s: str) -> int:
            m = cn_time_pat.match(s)
            if not m: raise ValueError(f"bad time format: {s!r}")
            h, mi, se = (int(x) if x else 0 for x in m.groups())
            return h * 3600 + mi * 60 + se
        try:
            ep_details = self.saferequestsget(params={"video_id": ep.video_id})['data']
            ep.title = ep_details['info']['chapter_title']
            ep.duration_sec = to_sec(ep_details['info'].get("duration"))
            ep.play_url = ep_details['url']
            ep.extra = ep_details
            return ep.play_url
        except:
            raise RuntimeError("Fail to fetch play url.")