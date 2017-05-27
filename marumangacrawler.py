import requests
import urllib
from bs4 import  BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='1111', db='moatoon', charset='utf8',autocommit=True)
curs = conn.cursor()

r = open('./marutoonlinklist.txt', 'r')
now = datetime.now()
file_path01 = "./marutoonlist.txt"
t = open(file_path01, 'w', encoding='utf-8')
ur = r.read()
url1=ur.split()
cn=0
hwalist=''
urls = [
]
for u in url1:
    cn+=1
    urls.append(u)

class MainParser:
    def __init__(self, func=None):
        if func:
            self.parse_url = func

def maru_parser(_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list = soup.select('div.content')
    minus = soup.select('div.gallery.bbs div')
    li = list[0].findAll('div')
    cnt = 2
    while cnt > 1 and cnt < len(li) - 3 - len(minus):
        a = li[cnt].findAll('a')
        for go in a:
            link = go['href']
            title = go.text
            print(link, title)
            hwalist="%s, %s\n"% (link,  title)
            sql = '''insert into toonlist(title, link) values("''' + go.text.strip() + '''","''' + go['href'] + '''")'''
            curs.execute(sql)
            t.write(hwalist)
        cnt += 1

    return data

parser_select_dict = {
    'marumaru.in': maru_parser
}


# def scraping():
data = ''
for url in urls:
    parsed_url = urlparse(url)
    print(parsed_url[1])
    func = parser_select_dict[parsed_url[1]]
    parser = MainParser(func)
    print(parser.parse_url(url))
t.close()

# if __name__ == '__main__':
#     scheduler = BlockingScheduler()
#     print("START")
#     scheduler.add_job(scraping, 'interval', seconds=10)
#
#     try:
#         scheduler.start()
#     except(KeyboardInterrupt, SystemExit):
#         print("EXIT")
#         pass