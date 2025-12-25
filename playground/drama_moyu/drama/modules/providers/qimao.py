'''
Function:
    Implementation of QiMaoProvider
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


'''QiMaoProvider'''
class QiMaoProvider(BaseProvider):
    source = 'QiMaoProvider'
    api_urls = [
        "https://api-v2.cenguigui.cn/api/duanju/qimao/", "https://api-v1.cenguigui.cn/api/duanju/qimao/", 
        "https://api.cenguigui.cn/api/duanju/qimao/", "https://player.cenguigui.cn/api/duanju/qimao/", 
    ]
    def __init__(self):
        super(QiMaoProvider, self).__init__()
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestsget(params={"name": query, "page": page})['data']['list']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['id'], title=search_result['title'], desc=f"{search_result['sub_title']}, {search_result['total_num']}, {search_result['label_name']}",
                    cover=search_result['image_link'], tags=search_result['sub_title'], engine=self.source, extra=search_result,
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={"id": drama.id})['data']
        drama.title = drama_details.get('title') or drama.title
        drama.desc = drama_details.get('intro') or drama.desc
        drama.cover = drama_details.get('image_link') or drama.cover
        drama.tags = drama_details.get('tags') or drama.tags
        drama.author = drama_details.get('creator') or drama.author
        drama.total_eps = self.safeint(drama_details.get("total_episode_num")) or drama.total_eps
        # iter to fetch
        play_list: list[dict] = drama_details.get("play_list") or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            sort = self.safeint(it.get("sort"))
            epno = sort if sort is not None else (i + 1)
            eps.append(Episode(
                ep=epno, title=f"第{epno}集", duration_sec=self.safeint(it.get("duration")), play_url=it.get("video_h265_url") or it.get("video_url"),
                video_id=str(it.get("video_id", "") or ""), extra=it,
            ))
        # return
        drama.total_eps = (len(eps) if eps else None) or drama.total_eps
        drama.episodes = eps
        return eps
    '''getplayurl'''
    def getplayurl(self, drama: Drama, ep: Episode) -> str:
        if ep.play_url: return ep.play_url
        eps = self.listepisodes(drama)
        for e in eps:
            if e.ep == ep.ep and e.play_url: return e.play_url
        raise RuntimeError("Fail to fetch play url.")