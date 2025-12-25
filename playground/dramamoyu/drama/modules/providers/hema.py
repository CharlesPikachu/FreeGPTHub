'''
Function:
    Implementation of HeMaProvider
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


'''HeMaProvider'''
class HeMaProvider(BaseProvider):
    source = 'HeMaProvider'
    api_urls = [
        "https://api-v2.cenguigui.cn/api/duanju/hema.php", "https://api-v1.cenguigui.cn/api/duanju/hema.php",
        "https://api.cenguigui.cn/api/duanju/hema.php", "https://player.cenguigui.cn/api/duanju/hema.php",
    ]
    def __init__(self):
        super(HeMaProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={"name": query, "page": page})['data']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['book_id'], title=search_result['title'], desc=search_result['intro'], cover=search_result['cover'], 
                    tags=", ".join([item['name'] for item in search_result['type']]), engine=self.source, extra=search_result, 
                    author=search_result['author'], total_eps=search_result['totalChapterNum']
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
        drama.tags = drama.tags
        drama.author = drama.author
        drama.total_eps = self.safeint(drama_details.get("total")) or drama.total_eps
        # iter to fetch
        play_list: list[dict] = drama_details.get("data") or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            ep_details: dict = self.saferequestsget(params={"book_id": drama.id, "video_id": it['video_id']})
            it['ep_details'] = ep_details
            sort = self.safeint(it['video_id'])
            epno = sort if sort is not None else (i + 1)
            eps.append(Episode(
                ep=epno, title=str(it.get("title", "") or f"第{epno}集"), duration_sec=60, play_url=ep_details['data']['url'],
                video_id=str(it.get("video_id", "") or ""), extra=it,
            ))
        # return
        drama.total_eps = (len(eps) if eps else None) or drama.total_eps
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        try:
            ep_details = self.saferequestsget(params={"book_id": drama.id, "video_id": ep.video_id})
            ep.title = ep_details['data']['title']
            ep.play_url = ep_details['data']['url']
            return ep.play_url
        except:
            raise RuntimeError("Fail to fetch play url.")
