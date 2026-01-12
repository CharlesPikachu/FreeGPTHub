'''
Function:
    Implementation of HongGuoProvider
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


'''HongGuoProvider'''
class HongGuoProvider(BaseProvider):
    source = 'HongGuoProvider'
    api_urls = ["https://api.xingzhige.com/API/playlet/"]
    def __init__(self):
        super(HongGuoProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={"keyword": query, "page": page})['data']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['book_id'], title=search_result['title'], desc=search_result['desc'], cover=search_result['cover'], author=search_result['author'],
                    tags=search_result['category_schema'], total_eps=None, episodes=[], engine=self.source, extra=search_result, 
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={"book_id": drama.id})['data']
        drama.title = drama.title or drama_details['detail'].get('title')
        drama.desc = drama.desc or drama_details['detail'].get('desc')
        drama.cover = drama.cover or drama_details['detail'].get('cover')
        drama.author = drama.author or ""
        drama.tags = drama.tags or drama_details['detail'].get('category_schema')
        drama.total_eps = drama.total_eps or drama_details['detail'].get('total')
        # iter to fetch
        play_list: list[dict] = drama_details['video_list'] or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            ep_details: dict = self.saferequestsget(params={"video_id": it['video_id'], "quality": "1080p"})['data']
            it['ep_details'] = ep_details
            epno = i + 1
            eps.append(Episode(
                ep=epno, title=f'{drama.title} 第{epno}集', duration_sec=it['duration'], play_url=ep_details['video']['url'], video_id=it['video_id'], extra=it,
            ))
        # return
        drama.total_eps = (len(eps) if eps else None) or drama.total_eps
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        try:
            ep_details: dict = self.saferequestsget(params={"video_id": ep.video_id, "quality": "1080p"})['data']
            return ep_details['video']['url']
        except:
            raise RuntimeError("Fail to fetch play url.")