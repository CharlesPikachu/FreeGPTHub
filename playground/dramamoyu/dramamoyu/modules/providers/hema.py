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
    api_urls = ["https://www.kuaikaw.cn"]
    def __init__(self):
        super(HeMaProvider, self).__init__()
        self.session.headers = {
            "accept": "*/*", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "connection": "keep-alive",
            "content-type": "application/json", "host": "www.kuaikaw.cn", "origin": "https://www.kuaikaw.cn", "pname": "www.kuaikaw.cn",
            "referer": "https://www.kuaikaw.cn", "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
    '''search'''
    def search(self, query: str, page: int = 1) -> List[Drama]:
        search_results = self.saferequestspost(json={"sourceType": 1, "keyword": query, "index": page}, suffix='/seo/video/6007')['data']['bookList']
        outputs: List[Drama] = []
        for search_result in search_results:
            try:
                output = Drama(
                    id=search_result['bookId'], title=search_result['bookName'], desc=search_result['introduction'], cover=search_result['coverWap'], 
                    author=", ".join([a for a in [search_result['actor'], search_result['actress']] if a]), 
                    tags=", ".join([item['name'] for item in search_result['bookTypeThree']]) if search_result['bookTypeThree'] else "", 
                    total_eps=search_result['totalChapterNum'], episodes=[], engine=self.source, extra=search_result, 
                )
            except:
                continue
            outputs.append(output)
        return outputs
    '''listepisodes'''
    def listepisodes(self, drama: Drama) -> List[Episode]:
        # update drama info
        drama_details: dict = self.saferequestsget(params={"bookId": drama.id}, suffix=f'/_next/data/hmjc_20251016/drama/{drama.id}.json')['pageProps']
        drama.title = drama.title or drama_details['bookInfoVo'].get('bookName')
        drama.desc = drama.desc or drama_details['bookInfoVo'].get('introduction')
        drama.cover = drama.cover or drama_details['bookInfoVo'].get('coverWap')
        drama.author = drama.author or ", ".join([a for a in [drama_details['bookInfoVo'].get('actor'), drama_details['bookInfoVo'].get('actress')] if a])
        drama.tags = drama.tags or (", ".join([item['name'] for item in drama_details['bookInfoVo'].get('bookTypeThree')]) if drama_details['bookInfoVo'].get('bookTypeThree') else "")
        drama.total_eps = drama.total_eps or self.safeint(drama_details['bookInfoVo'].get("totalChapterNum"))
        # iter to fetch
        play_list: list[dict] = drama_details.get("chapterList") or []
        eps: List[Episode] = []
        pbar = tqdm(enumerate(play_list))
        for i, it in pbar:
            pbar.set_description(f'Process Episode {i+1}')
            sort = self.safeint(it.get("chapterIndex"))
            epno = sort if sort is not None else (i + 1)
            if 'chapterVideoVo' not in it: continue
            eps.append(Episode(
                ep=epno, title=f'{drama.title} 第{epno}集', duration_sec=None, play_url=it['chapterVideoVo'].get('vodMp4Url') or it['chapterVideoVo'].get('mp4720p') or it['chapterVideoVo'].get('mp4'), video_id=it.get("chapterId", "") or f"{drama.id}-{epno}", extra=it,
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
