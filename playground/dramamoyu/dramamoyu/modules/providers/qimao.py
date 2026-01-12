'''
Function:
    Implementation of QiMaoProvider
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import base64
from tqdm import tqdm
from typing import List
from .base import BaseProvider
from ..utils import Drama, Episode


'''QiMaoProvider'''
class QiMaoProvider(BaseProvider):
    source = 'QiMaoProvider'
    api_urls = ["https://sdkapi.hhlqilongzhu.cn/api/qimao_duanju/"]
    secret_key = base64.b64decode(b'RHJhZ29uOTQzMDEyNDA4MUZFQUJGQTYyNjg4NEJEMjhBRjFCREY=').decode('utf-8')
    def __init__(self):
        super(QiMaoProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={'key': QiMaoProvider.secret_key, 'name': query, 'page': page})['data']['list']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['id'], title=search_result['title'], desc=f"{search_result['sub_title']}, {search_result['total_num']}, {search_result['label_name']}, {search_result['hot_value']}", cover=search_result['image_link'], 
                    author=search_result['actor'] or "", tags=search_result['sub_title'], total_eps=self.safeint(search_result['label_name'].replace('集', '')), episodes=[], engine=self.source, extra=search_result, 
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={'key': QiMaoProvider.secret_key, 'id': drama.id})['data']
        drama.title = drama.title or drama_details.get('title')
        drama.desc = drama.desc or drama_details.get('intro')
        drama.cover = drama.cover or drama_details.get('image_link')
        drama.author = drama.author or drama_details.get('creator')
        drama.tags = drama.tags or drama_details.get('tags')
        drama.total_eps = drama.total_eps or self.safeint(drama_details.get('total_num'))
        # iter to fetch
        play_list: list[dict] = drama_details.get("play_list") or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            sort = self.safeint(it.get("sort"))
            epno = sort if sort is not None else (i + 1)
            eps.append(Episode(
                ep=epno, title=f'{drama.title} 第{epno}集', duration_sec=self.safeint(it.get("duration")), play_url=it.get("video_h265_url") or it.get("video_url"), video_id=it.get("video_id") or f"{drama.id}-{epno}", extra=it,
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