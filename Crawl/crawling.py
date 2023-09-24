from bs4 import BeautifulSoup
from requests import * 
import time
import re
import os
import csv
import os.path
import json
from tqdm import tqdm
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import threading

Path = f'./news_contents.csv'
if os.path.isfile(Path):
    print("news_contents 파일 있어요")
    f = open(f"{Path}", 'r')
    lines = f.readlines()
len(lines)

df = pd.read_json('naver_news_pages.json')

# 크롤링 함수 정의
def parallel_crawl(df):
    sema = threading.Semaphore(5)
    result = []
    bad = []
    def get_page_data(idx):
        sema.acquire()
        target = df.iloc[idx]   
        category = target["media"]
        date = target["date"]
        url = target["url"]
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        }
        try:
            article_response = requests.get(url, headers=headers)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            article_title = article_soup.select_one("h2.media_end_head_headline").text
            article_content = article_soup.select_one("#newsct_article").text
            article_content  = article_content .replace("\n",'')
            article_content  = article_content .replace("\t",'')
            media = article_soup.select_one("em.media_end_linked_more_point").text
            date = article_soup.select_one("div.media_end_head_info_datestamp").text.strip()
            date = date.replace("\n",'')
            date = date.replace("기사원문",'')
            reporter = article_soup.select_one("span.byline_s").text

            stick_q_1 = url.split("article",1)[1][1:].split("/",1)[0]
            stick_q_2 = url.split("article",1)[1][1:].split("/",1)[1].split("?",1)[0]

            stick_base = "https://news.like.naver.com/v1/search/contents?"

            stick_dict = {
                "touched":0,
                "analytical": 0,
                "wow": 0,
                "recommend": 0,
                "useful": 0
                }

            stick_params = {
                'suppress_response_codes': 'true',
                'callback': 'jQuery3310448700715771974_1694708654510',
                'q': f'NEWS[ne_{stick_q_1}_{stick_q_2}]',
                'isDuplication': 'false',
                'cssIds': 'MULTI_MOBILE,NEWS_MOBILE',
                '_': 1694708654511,
            }

            stick_get = requests.get(stick_base, params = stick_params, headers=headers)
            time.sleep(1)
            for idx in range(len(stick_get.text)):
                if stick_get.text[idx] == "{":
                    x = idx
                    break
            for idx in range(len(stick_get.text)-1,0,-1):
                if stick_get.text[idx] == "}":
                    y = idx
                    break
            stick = json.loads(stick_get.text[x:y+1])
            stick_list = stick["contents"][-1].get("reactions")
            for stick_info in stick_list:
                target_stick = stick_info["reactionType"]
                stick_score = stick_info["count"]
                stick_dict[target_stick] = stick_score

            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                'Referer': url 
            }
            
            with open('news_contents.csv', 'a', encoding='utf-8') as f:
                f.write(f'{category}_[이성현]_{url}_[이성현]_{date}_[이성현]_{article_title}_[이성현]_{article_content}_[이성현]_{media}_[이성현]_{reporter}_[이성현]_{stick_dict["touched"]}_[이성현]_{stick_dict["analytical"]}_[이성현]_{stick_dict["wow"]}_[이성현]_{stick_dict["recommend"]}_[이성현]_{stick_dict["useful"]}\n')
            
            maybe_2 = url.split("article",1)[1].split("?",1)[1]
            maybe_1 = url.split("article",1)[1].split("?",1)[0]
            maybe = url.split("article",1)[0]
            target_test = maybe + "article/" +"comment"+ maybe_1 + "?" + maybe_2
            testrespone = requests.get(target_test, headers=headers)
            newid_1 = maybe_1[1:].split('/',1)[0]
            newid_2 = maybe_1[1:].split('/',1)[1]

            test_soup = BeautifulSoup(testrespone.content, 'html.parser')

            url_info =  "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?"

            params = {
                'ticket': 'news',
                'templateId': 'default_society',
                'pool': 'cbox5',
                '_cv': 20230912182421,
                '_callback': 'jQuery33103549467654035898_1694663205565',
                'lang': 'ko',
                'country': 'KR',
                'objectId': f'news{newid_1},{newid_2}',
                'categoryId': None,
                'pageSize': 20,
                'indexSize': 10,
                'groupId': None,
                'listType': 'OBJECT',
                'pageType': 'more',
                'page': 1,
                # 'currentPage': 3,
                'refresh': 'false',
                'sort': 'FAVORITE',
                # 'current': 803130716614295740,
                # 'prev': 803125437143187665,
                # 'moreParam.direction': next,
                # 'moreParam.prev': '100001u00001u063nw7geerd1t',
                # 'moreParam.next': '1000000000000063ny2tr7jni4',
                'includeAllStatus': 'true',
                '_': 1694663205571,
            }

            coment_req = requests.get(url_info, params = params, headers=headers)
            for idx in range(len(coment_req.text)):
                if coment_req.text[idx] == "{":
                    x = idx
                    break
            for idx in range(len(coment_req.text)-1,0,-1):
                if coment_req.text[idx] == "}":
                    y = idx
                    break
            com = json.loads(coment_req.text[x:y+1])

            li_list = com["result"].get("commentList")
            coment_list = []
            if not li_list:
                pass
            else:
                coment_info_list = []
                for infos in com["result"].get('commentList'):
                    word = infos["contents"]
                    id_num = infos["userIdNo"]
                    comment_word = infos["contents"]
                    comment_date = infos["regTime"][:-5]
                    coment_info = [word, url, comment_word, id_num,comment_date]
                    coment_info_list.append(coment_info)
                    
                prev = com["result"].get("morePage")['prev']
                next1 = com["result"].get("morePage")['next']
                start = com["result"].get("morePage")['start']
                end = com["result"].get("morePage")['end']
                epho = com["result"].get("pageModel")["totalRows"]
                if epho > 20:
                    count = epho - 20
                    start_page = 0
                    while True:
                        start_page += 1
                        params = {
                            'ticket': 'news',
                            'templateId': 'default_society',
                            'pool': 'cbox5',
                            '_cv': 20230912182421,
                            '_callback': 'jQuery33103549467654035898_1694663205565',
                            'lang': 'ko',
                            'country': 'KR',
                            'objectId': f'news{newid_1},{newid_2}',
                            'categoryId': None,
                            'pageSize': 20,
                            'indexSize': 10,
                            'groupId': None,
                            'listType': 'OBJECT',
                            'pageType': 'more',
                            'page': start_page,
                            # 'currentPage': 3,
                            'refresh': 'false',
                            'sort': 'FAVORITE',
                            'current': 803130716614295740,
                            'prev': 803125437143187665,
                            'moreParam.direction': 'next',
                            'moreParam.prev': prev,
                            'moreParam.next': next1,
                            'includeAllStatus': 'true',
                            '_': 1694663205571,
                        }

                        temp = requests.get(url_info, params = params, headers=headers)
                        for idx in range(len(temp.text)):
                            if temp.text[idx] == "{":
                                x = idx
                                break
                        for idx in range(len(temp.text)-1,0,-1):
                            if temp.text[idx] == "}":
                                y = idx
                                break
                        com = json.loads(temp.text[x:y+1])
                        li_list = com["result"].get("commentList")
                        for content in li_list:
                            coment_list.append(content["contents"])

                        for infos in com["result"].get('commentList'):
                            word = infos["contents"]
                            id_num = infos["userIdNo"]
                            comment_word = infos["contents"]
                            comment_date = infos["regTime"][:-5]
                            coment_info = [url, comment_word, id_num,comment_date]
                            coment_info_list.append(coment_info)
                        coment_list = [content["commentNo"] for content in com["result"].get('commentList')]
                        try:
                            for comment_no in coment_list:
                                comment_user_url_base = "https://apis.naver.com/commentBox/cbox/web_naver_user_info_jsonp.json?"
                                users_params = {
                                    'ticket': 'news',
                                    'templateId': 'default_society',
                                    'pool': 'cbox5',
                                    '_cv': 20230912182421,
                                    '_callback': 'jQuery33103549467654035898_1694663205565',
                                    'lang': 'ko',
                                    'country': 'KR',
                                    'objectId': f'news{newid_1},{newid_2}',
                                    'categoryId': None,
                                    'pageSize': 20,
                                    'indexSize': 10,
                                    'groupId': None,
                                    'listType': 'user',
                                    'pageType': 'more',
                                    # 'currentPage': 3,
                                    'refresh': 'false',
                                    'sort': 'FAVORITE',
                                    'current': 803130716614295740,
                                    'prev': 803125437143187665,
                                    'moreParam.direction': 'next',
                                    'commentNo': comment_no,
                                    'targetUserInKey': None,
                                    'includeAllStatus': 'true',
                                    '_': 1694663205571,
                                }
                                another_commnet = requests.get(comment_user_url_base, params = users_params, headers=headers)
                                for idx in range(len(another_commnet.text)):
                                    if another_commnet.text[idx] == "{":
                                        x = idx
                                        break
                                for idx in range(len(another_commnet.text)-1,0,-1):
                                    if another_commnet.text[idx] == "}":
                                        y = idx
                                        break
                                another_com = json.loads(another_commnet.text[x:y+1])
                                another_com_list = another_com["result"].get('commentList')
                                for contents in another_com_list:
                                    another_content = contents["contents"]
                                    another_content  = another_content.replace("\n",'')
                                    another_content  = another_content.replace("\t",'')
                                    user_id = contents["idNo"]
                                    another_date = contents["modTime"]
                                    another_url = contents["objectUrl"]
                                    another_Category = contents["objectCategoryName"]
                                    with open('user_another_comments.csv', 'a', encoding='utf-8') as f:
                                        f.write(f'{another_Category}_[이성현]_{another_url}_[이성현]_{another_content}_[이성현]_{user_id}_[이성현]_{another_date}\n')
                        except:
                            pass
                        prev = com["result"].get("morePage")['prev']
                        next1 = com["result"].get("morePage")['next']
                        start = com["result"].get("morePage")['start']
                        end = com["result"].get("morePage")['end']
                        count -= 20
                        if 0 >= count:
                            break

                else:
                    pass
                for idx_i in range(len(coment_info_list)):
                    target = coment_info_list[idx_i]
                    coment_word = target[0]
                    coment_word  = coment_word.replace("\n",'')
                    coment_word  = coment_word.replace("\t",'')
                    coment_url = target[1]
                    coment_id = target[3]
                    coment_date = target[4]
                    with open('user_comments.csv', 'a', encoding='utf-8') as f:
                        f.write(f'{category}_[이성현]_{coment_url}_[이성현]_{coment_word}_[이성현]_{coment_id}_[이성현]_{coment_date}\n')
        except:
            with open('bug_log.csv', 'a', encoding='utf-8') as f:
                f.write(f'{idx}\n')
        sema.release()

    thread_list = [threading.Thread(target=get_page_data, args=(idx, )) 
                    for idx in range(len(lines)-1,len(df))]
    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    return bad

bad = parallel_crawl(df)
for i in result:
    with open('bug_log.csv', 'a', encoding='utf-8') as f:
        f.write(f'{i}\n')