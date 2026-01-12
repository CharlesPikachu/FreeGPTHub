'''
Function:
    Implementation of WeiGuanProvider
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import json_repair
from tqdm import tqdm
from typing import List
from .base import BaseProvider
from ..utils import Drama, Episode


'''WeiGuanProvider'''
class WeiGuanProvider(BaseProvider):
    source = 'WeiGuanProvider'
    api_urls = ["https://api.drama.9ddm.com/drama/home"]
    def __init__(self):
        super(WeiGuanProvider, self).__init__()
        self.session.headers = {"User-Agent": "okhttp/3.12.11", "Content-Type": "application/json; charset=utf-8", "Accept": "application/json"}
    '''search'''
    def search(self, query: str, page: int = 1, page_size: int = 30) -> List[Drama]:
        payload = {"audience": "", "page": page, "pageSize": page_size, "searchWord": query, "subject": ""}
        search_results = self.saferequestspost(json=payload, suffix='/search')['data']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['oneId'], title=search_result['title'], desc=search_result['description'], cover=search_result['horzPoster'] or search_result['vertPoster'], 
                    author=', '.join(search_result['actors']) if search_result['actors'] else "", tags=', '.join(search_result['shortPlayTag']) if search_result['shortPlayTag'] else "", 
                    total_eps=None, episodes=[], engine=self.source, extra=search_result, 
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={"oneId": drama.id, "page": 1, "pageSize": 1000}, suffix='/shortVideoDetail')
        drama.title = drama.title or drama_details.get('title')
        drama.desc = drama.desc or drama_details.get('desc')
        drama.cover = drama.cover or drama_details.get('vertPoster')
        drama.author = drama.author or (', '.join(drama_details.get('actors')) if drama_details.get('actors') else "")
        drama.tags = drama.tags or (', '.join(drama_details.get('shortPlayTag')) if drama_details.get('shortPlayTag') else "")
        drama.total_eps = drama.total_eps or self.safeint(drama_details.get("totalEpisodeCount"))
        # iter to fetch
        play_list: list[dict] = drama_details.get("data") or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            sort = self.safeint(it.get("playOrder"))
            epno = sort if sort is not None else (i + 1)
            play_settings = json_repair.loads(it['playSetting'])
            eps.append(Episode(
                ep=epno, title=f'{it.get("title", "")} 第{epno}集', duration_sec=it.get("playLength"), play_url=play_settings.get("super") or play_settings.get("high") or play_settings.get("normal"), video_id=it.get("episodeOneId") or f"{drama.id}-{epno}", extra=it,
            ))
        # return
        drama.total_eps = drama.total_eps or len(eps)
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        try:
            eps: List[Episode] = self.listepisodes(drama=drama)
            for item in eps:
                if item.video_id == ep.video_id or item.ep == ep.ep: return ep.play_url
        except:
            raise RuntimeError("Fail to fetch play url.")