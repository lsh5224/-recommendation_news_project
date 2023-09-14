import scrapy
from daum_news.items import DaumNewsItem
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin
import json

class DaumNewsSpider(scrapy.Spider):
    
    name = 'daum_news'
    topics = ['finance', 'industry', 'employ', 'others', 'autos', 'stock', 'stock/market', 'stock/publicnotice', 'stock/world', 'stock/bondsfutures','stock/fx', 'stock/others', 'estate', 'consumer','world']
    base_url = 'https://news.daum.net/breakingnews/economic/{}?page={}&regDate={}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    headers.update({
    'Authorization' :'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb3J1bV9rZXkiOiJuZXdzIiwidXNlcl92aWV3Ijp7ImlkIjoxODA2NDU3NSwiaWNvbiI6Imh0dHBzOi8vdDEuZGF1bWNkbi5uZXQvcHJvZmlsZS80el9Ta2xqcUp6bzAiLCJwcm92aWRlcklkIjoiREFVTSIsImRpc3BsYXlOYW1lIjoi7Jik7Jik7Jik7Ji5In0sImdyYW50X3R5cGUiOiJhbGV4X2NyZWRlbnRpYWxzIiwic2NvcGUiOltdLCJleHAiOjE2OTQ3MTY4NjQsImF1dGhvcml0aWVzIjpbIlJPTEVfSU5URUdSQVRFRCIsIlJPTEVfREFVTSIsIlJPTEVfSURFTlRJRklFRCIsIlJPTEVfVVNFUiJdLCJqdGkiOiJmZjY0OGFjMy1lZjE3LTQ4NmEtYmVmMi1iZWMzODE5OTcxMTgiLCJmb3J1bV9pZCI6LTk5LCJjbGllbnRfaWQiOiIyNkJYQXZLbnk1V0Y1WjA5bHI1azc3WTgifQ.6nzz1CcFRcXryw0xnzO78Me7Fwtkq1ZvImCexPZByJs'
})
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 1)
    
    #finance(금융), industry(기업산업), employ(취업직장인), others(경제일반), autos(자동차)
    #stock(주식), stock/market(시황분석), stock/publicnotice(공시), stock/world(해외증시), stock/bondsfutures(채권선물)
    #stock/fx(외환), stock/others(주식일반), estate(부동산), consumer(생활경제), world(국제경제)


    #날짜 및 세부카테고리만 지정한 URL 생성, parse함수 실행
    def start_requests(self):

        for topic in self.topics:

            self.detail_topic = topic
            current_date = self.start_date

            while current_date <= self.end_date:
                date = current_date.strftime('%Y%m%d')
                url = self.base_url.format(topic, 1, date)
                yield scrapy.Request(url=url, callback=self.parse, headers=self.headers, meta={'page': 1, 'topic': topic, 'current_date': date})
                current_date += timedelta(days=1)

    #각 페이지별 기사 링크 크롤링 진행
    def parse(self, response):
        # 현재 페이지의 기사 제목들을 기준으로 중복 여부 판별
        titles_current = response.css('div.box_etc > ul > li> div > strong > a::text').getall()
        if titles_current == response.meta.get('titles_prev', []):
            return

        # 기사 링크 크롤링 진행
        detail_urls = response.css('#mArticle > div.box_etc > ul > li > a::attr(href)').getall()
        for detail_url in detail_urls:
            self.detail_url = detail_url
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, headers=self.headers, meta={'detail_topic': response.meta['topic'], 'detail_url': detail_url})

        # 다음 페이지로 이동
        next_page = response.meta['page'] + 1
        next_url = self.base_url.format(response.meta['topic'], next_page, response.meta['current_date'])
        yield scrapy.Request(url=next_url, callback=self.parse, headers=self.headers, meta={'page': next_page, 'topic': response.meta['topic'], 'current_date': response.meta['current_date'], 'titles_prev': titles_current})

    # 각 기사 제목, 내용, 신문사 크롤링 진행
    def parse_detail(self, response):

        date = self.start_date.strftime('%Y-%m-%d')
        title = response.css('#mArticle > div.head_view > h3::text').get()
        contents = response.xpath('//*[@id="mArticle"]/div[2]/div[2]/section/p/text()').getall()
        company = response.xpath('//*[@id="kakaoServiceLogo"]/text()').get()

        item = DaumNewsItem()
        item['URL'] = response.meta['detail_url']
        item['TITLE'] = title
        item['CAT_BIG'] = 'economy'
        item['CAT_SMALL'] = response.meta['detail_topic']
        item['PRESS'] = company
        item['DATE'] = date
        item['CONTENTS'] =contents

        #각 뉴스기사별 감정 스티커 json url 추출
        sticker_key = re.search(r'(\d+)', response.meta['detail_url']).group(1)
        sticker_base_url = "https://action.daum.net/apis/v1/reactions/"
        endpoint = f"home?itemKey={sticker_key}"
        sticker_url = urljoin(sticker_base_url, endpoint)
        yield scrapy.Request(url=sticker_url, callback=self.emotion_sticker, headers=self.headers, meta={'item': item})
        
    def emotion_sticker(self, response):
        data = json.loads(response.text)
        item = response.meta['item']

        item["LIKE"] = data["item"]["stats"]["LIKE"]
        item['DISLIKE'] = data['item']["stats"]["DISLIKE"]
        item['GREAT'] = data["item"]["stats"]["GREAT"]
        item['SAD'] = data["item"]["stats"]["SAD"]
        item['ABSURD'] = data["item"]["stats"]["ABSURD"]
        item['ANGRY'] = data["item"]["stats"]["ANGRY"]
        item['RECOMMEND'] = data["item"]["stats"]["RECOMMEND"]
        item['IMPRESS'] = data["item"]["stats"]["IMPRESS"]

        yield item
