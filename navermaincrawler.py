import requests
import urllib
import pymysql
from bs4 import  BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler


conn = pymysql.connect(host='localhost', user='root', password='1111', db='moatoon', charset='utf8',autocommit=True)
curs = conn.cursor()
urls = [
'http://comic.naver.com/webtoon/weekdayList.nhn?week=mon',
'http://comic.naver.com/webtoon/weekdayList.nhn?week=tue',
'http://comic.naver.com/webtoon/weekdayList.nhn?week=wed',
'http://comic.naver.com/webtoon/weekdayList.nhn?week=thu',
'http://comic.naver.com/webtoon/weekdayList.nhn?week=fri',
'http://comic.naver.com/webtoon/weekdayList.nhn?week=sat',
'http://comic.naver.com/webtoon/weekdayList.nhn?week=sun',
'http://comic.naver.com/webtoon/finish.nhn'
]
class MainParser:
    def __init__(self, func=None):
        if func:
            self.parse_url = func

def naver_parser(_url):
    response = requests.get(_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list = soup.select('ul.img_list li')
    cnt = 1
    data = ''
    tlist = ''
    for li in list:
        li2 = li.find_all('a')
        thumb = li.find('img')['src']
        # print(cnt, thumb, li2[1].text.strip(), li2[2].text.strip(), 'http://comic.naver.com' + li2[1]['href'])
        data = "[%3d번째 웹툰] 썸네일주소 : %s, 웹툰명 : %s, 작가명 : %s, 웹툰주소 : %s\n" % \
                (cnt, thumb, li2[1].text.strip(), li2[2].text.strip(), 'http://comic.naver.com' + li2[1]['href'])
        tlist = "%s\n" % ("http://comic.naver.com" + li2[1]['href']+'&page=')
        sql = "insert into mainlist(site, title, author, thumb) values('daum','"+li2[1].text.strip()+"','"+li2[2].text.strip()+"','"+thumb+"')"
        curs.execute(sql)
        f.write(data)
        t.write(tlist)
        cnt = cnt + 1
    return data

parser_select_dict = {
    'comic.naver.com': naver_parser
}

now = datetime.now()
file_path = datetime.strftime(now, "./toonlist01.txt")
file_path01 = "./toonlinklist.txt"
# def scraping():
data = ''
f = open(file_path, 'w', encoding='utf-8')
t = open(file_path01, 'w', encoding='utf-8')
for url in urls:
    parsed_url = urlparse(url)
    print(parsed_url[1])
    func = parser_select_dict[parsed_url[1]]
    parser = MainParser(func)
    print(parser.parse_url(url))
f.close()
t.close()
conn.close()