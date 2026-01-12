'''
Function:
    Implementation of BaiDuProvider
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


'''BaiDuProvider'''
class BaiDuProvider(BaseProvider):
    source = 'BaiDuProvider'
    api_urls = ["https://api-v2.cenguigui.cn/api/duanju/baidu/", "https://api-v1.cenguigui.cn/api/duanju/baidu/", "https://api.cenguigui.cn/api/duanju/baidu/", "https://player.cenguigui.cn/api/duanju/baidu/"]
    def __init__(self):
        super(BaiDuProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={"name": query, "page": page})['data']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['id'], title=search_result['title'], desc="", cover=search_result['cover'], author="", tags="", 
                    total_eps=search_result['totalChapterNum'], episodes=[], engine=self.source, extra=search_result, 
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={"id": drama.id})
        drama.title = drama.title or drama_details.get('title')
        drama.desc = drama.desc
        drama.cover = drama.cover
        drama.author = drama.author
        drama.tags = drama.tags
        drama.total_eps = drama.total_eps or self.safeint(drama_details.get("total"))
        # iter to fetch
        play_list: list[dict] = drama_details.get("data") or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        replace_title_func = lambda s: (lambda t: (lambda u: (lambda v: re.sub(r'\s*(?:[-—_#.:：\s]+)\s*\d{1,3}\s*$', '', v).strip())(re.sub(r'\s*[\(\（\[\【\{]\s*\d{1,4}\s*[\)\）\]\】\}]\s*$', '', u).strip()))(re.sub(r'\s*第\s*\d{1,4}\s*(?:集|话|章|篇|卷|期|季)\s*$', '', t).strip()))(s.strip())
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            ep_details: dict = self.saferequestsget(params={"video_id": it['video_id']})
            it['ep_details'] = ep_details
            epno = i + 1
            eps.append(Episode(
                ep=epno, title=f'{replace_title_func(it.get("title", ""))} 第{epno}集', duration_sec=ep_details['data']['duration'], play_url=ep_details['data']['qualities'][-1]['download_url'], video_id=it['video_id'], extra=it,
            ))
        # return
        drama.author = drama.author or ep_details['data']['author']['name'] or ""
        drama.total_eps = drama.total_eps or len(eps)
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        try:
            ep_details = self.saferequestsget(params={"video_id": ep.video_id})
            return ep_details['data']['qualities'][-1]['download_url']
        except:
            raise RuntimeError("Fail to fetch play url.")