'''
Function:
    Implementation of BaiDuProvider
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


'''BaiDuProvider'''
class BaiDuProvider(BaseProvider):
    source = 'BaiDuProvider'
    api_urls = [
        "https://api-v2.cenguigui.cn/api/duanju/baidu/", "https://api-v1.cenguigui.cn/api/duanju/baidu/",
        "https://api.cenguigui.cn/api/duanju/baidu/", "https://player.cenguigui.cn/api/duanju/baidu/",
    ]
    def __init__(self):
        super(BaiDuProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={"name": query, "page": page})['data']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['id'], title=search_result['title'], desc="", cover=search_result['cover'], tags="", 
                    engine=self.source, extra=search_result, total_eps=search_result['totalChapterNum']
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
        drama.desc = drama.desc
        drama.cover = drama.cover
        drama.tags = drama.tags
        drama.author = drama.author
        drama.total_eps = self.safeint(drama_details.get("total")) or drama.total_eps
        # iter to fetch
        play_list: list[dict] = drama_details.get("data") or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            ep_details: dict = self.saferequestsget(params={"video_id": it['video_id']})
            it['ep_details'] = ep_details
            epno = i + 1
            eps.append(Episode(
                ep=epno, title=str(it.get("title", "") or f"第{epno}集"), duration_sec=ep_details['data']['duration'], play_url=ep_details['data']['qualities'][-1]['download_url'],
                video_id=it['video_id'], extra=it,
            ))
        # return
        drama.author = ep_details['data']['author']['name']
        drama.total_eps = (len(eps) if eps else None) or drama.total_eps
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        try:
            ep_details = self.saferequestsget(params={"video_id": ep.video_id})
            ep.title = ep_details['data']['title']
            ep.duration_sec = ep_details['data']['duration']
            ep.play_url = ep_details['data']['qualities'][-1]['download_url']
            return ep.play_url
        except:
            raise RuntimeError("Fail to fetch play url.")