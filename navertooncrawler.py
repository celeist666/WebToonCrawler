import requests
import urllib
from bs4 import  BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import os
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler

conn = pymysql.connect(host='localhost', user='root', password='1111', db='moatoon', charset='utf8',autocommit=True)
curs = conn.cursor()
r = open('./toonlinklist.txt', 'r')
ur = r.read()
url1=ur.split()
cn=0
urls = [
]
for u in url1:
    cn+=1
    urls.append(u)

class MainParser:
    def __init__(self, func=None):
        if func:
            self.parse_url = func

    def parse_url(self, _url):
        print("미구현")
        print(_url)

def naver_parser(_url):
    number = 0
    stop = 1
    list2 = None
    # f = open(file_path, 'w', encoding='utf-8')
    while stop == 1:
        number += 1
        response = requests.get(_url + str(number))
        soup = BeautifulSoup(response.text, 'html.parser')
        list = soup.select('table tr')
        cnt = 1
        data = ''
        if list != list2:
            for li in list:
                # 후에 이 이프문 주소말고 조건으로 바꿔야함
                if _url + str(number) != "http://comic.naver.com/webtoon/list.nhn?titleId=25455&weekday=tue&page="+str(number) and _url  + str(number) != 'http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=tue&page='+str(number):
                    if cnt < 3:
                        cnt = cnt + 1
                        continue
                    li2 = li.find('img')['src']
                    title = li.find_all('a')
                    href = title[1]['href']
                    date = li.find_all('td')
                    print(li2, title[1].text, 'http://comic.naver.com' + href, date[3].text)
                    data = "%s, %s, %s, %s\n" % (li2, title[1].text, 'http://comic.naver.com' + href, date[3].text)
                    # 아래 sql은 제목에 '가 들어갔을경우 뻑나는걸 방지하기 위해 '''이 많음;
                    sql = '''insert into toonlist(title, link, date) values("''' + title[
                        1].text + '''","''' + href + '''","''' + date[3].text + '''")'''
                    curs.execute(sql)
                    f.write(data)
                else:
                    if cnt < 4:
                        cnt = cnt + 1
                        continue
                    li2 = li.find('img')['src']
                    title = li.find_all('a')
                    href = title[1]['href']
                    date = li.find_all('td')
                    print(li2, title[1].text, 'http://comic.naver.com' + href, date[3].text)
                    data = "%s, %s, %s, %s\n" % (li2, title[1].text, 'http://comic.naver.com' + href, date[3].text)
                    f.write(data)
        else:
            break
        list2 = list

    return data

parser_select_dict = {
    'comic.naver.com': naver_parser
}

now = datetime.now()
file_path = datetime.strftime(now, "./toon.txt")

# def scraping():
data = ''
f = open(file_path, 'w', encoding='utf-8')
for url in urls:
    parsed_url = urlparse(url)
    print(parsed_url[1], url)
    func = parser_select_dict[parsed_url[1]]
    parser = MainParser(func)
    # f.write(parser.parse_url(url))
    print(parser.parse_url(url))
f.close()
r.close()
conn.close()
# 아래는 반복실행을 위한 코드
# if __name__ == '__main__':
#     scheduler = BlockingScheduler()
#     print("START")
#     scheduler.add_job(scraping, 'interval', seconds=30)
#
#     try:
#         scheduler.start()
#     except(KeyboardInterrupt, SystemExit):
#         print("EXIT")
#         pass