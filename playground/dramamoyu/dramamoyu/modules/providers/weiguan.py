'''
Function:
    Implementation of WeiGuanProvider
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
from tqdm import tqdm
from typing import List
from .base import BaseProvider
from ..utils import Drama, Episode


'''WeiGuanProvider'''
class WeiGuanProvider(BaseProvider):
    source = 'WeiGuanProvider'
    api_urls = [
        "https://api-v2.cenguigui.cn/api/duanju/weiguan/", "https://api-v1.cenguigui.cn/api/duanju/weiguan/", 
        "https://api.cenguigui.cn/api/duanju/weiguan/", "https://player.cenguigui.cn/api/duanju/weiguan/", 
    ]
    def __init__(self):
        super(WeiGuanProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={"name": query, "page": page})['data']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['id'], title=search_result['title'], desc=search_result['intro'], cover=search_result['pic'], tags=search_result['type'], 
                    engine=self.source, extra=search_result, author=search_result['author']
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={"id": drama.id})
        drama.title = drama_details.get('title') or drama.title
        drama.desc = drama_details.get('desc') or drama.desc
        drama.cover = drama_details.get('pic') or drama.cover
        drama.tags = drama_details.get('category') or drama.tags
        drama.author = drama_details.get('author') or drama.author
        drama.total_eps = self.safeint(drama_details.get("total")) or drama.total_eps
        # iter to fetch
        play_list: list[dict] = drama_details.get("data") or []
        eps: List[Episode] = []
        to_sec = lambda t: sum(int(x) * 60**i for i, x in enumerate(reversed(t.split(':'))))
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            sort = self.safeint(it.get("playOrder"))
            epno = sort if sort is not None else (i + 1)
            eps.append(Episode(
                ep=epno, title=str(it.get("title", "") or f"第{epno}集"), duration_sec=to_sec(it.get("playLength")), play_url=it.get("MP4Url"),
                video_id=f"{drama.id}_{epno}", extra=it,
            ))
        # return
        drama.total_eps = (len(eps) if eps else None) or drama.total_eps
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        try:
            ep_details = self.saferequestsget(params={"id": drama.id, "playOrder": ep.ep})['data']
            ep.title = ep_details['title']
            ep.play_url = ep_details['url']
            return ep.play_url
        except:
            raise RuntimeError("Fail to fetch play url.")