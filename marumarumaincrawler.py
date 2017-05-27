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

urls = [
'http://marumaru.in/?c=1/40&p='
]
class MainParser:
    def __init__(self, func=None):
        if func:
            self.parse_url = func

def maru_parser(_url):
    number=0
    stop=1
    cnt=1
    while stop == 1:
        number += 1
        response = requests.get(url + str(number))
        soup = BeautifulSoup(response.text, 'html.parser')
        list = soup.select('div.picbox')

        data = ''
        tlist = ''
        if list != []:
            for li in list:
                li2 = li.find('div')
                # print(li2)
                li1 = li.find_all('div')
                thumb = li.find('img')['src']
                link= ''
                if len(li1[1].find('a').text.split(']')) != 3:
                    tit = li1[1].find('a').text.split(']')
                    print(cnt, thumb, tit[1], 'http://marumaru.in' + li2.find('a')['href'])
                    link = 'http://marumaru.in' + li2.find('a')['href']
                    data = "[%4d번째 망가] 썸네일주소 : %s, 웹툰명 : %s, 웹툰주소 : %s\n" % \
                           (cnt, thumb, tit[1], 'http://marumaru.in' + li2.find('a')['href'])
                    tlist = "%s\n" % ("http://marumaru.in" + li2.find('a')['href'])
                    sql = '''insert into mainlist(site, title, thumb,main_link) values("maru","''' + tit[
                        1].strip() + '''","''' + thumb + '''","'''+ link + '''")'''
                    curs.execute(sql)
                    f.write(data)
                    t.write(tlist)
                    cnt = cnt + 1
                else:
                    tit = li1[1].find('a').text.split(']')
                    print(cnt, thumb, tit[2].strip(), 'http://marumaru.in' + li2.find('a')['href'])
                    link = 'http://marumaru.in' + li2.find('a')['href']
                    data = "[%4d번째 망가] 썸네일주소 : %s, 웹툰명 : %s, 웹툰주소 : %s\n" % \
                            (cnt, thumb, tit[2].strip(), 'http://marumaru.in' + li2.find('a')['href'])
                    tlist = "%s\n" % ("http://marumaru.in" + li2.find('a')['href'])
                    sql = '''insert into mainlist(site, title, thumb,main_link) values("maru","''' + tit[
                        2].strip() + '''","''' + thumb + '''","''' + link + '''")'''
                    curs.execute(sql)
                    f.write(data)
                    t.write(tlist)
                    cnt = cnt + 1
        else:
            break

    return data

parser_select_dict = {
    'marumaru.in': maru_parser
}

now = datetime.now()
file_path = datetime.strftime(now, "./marutoonlist01.txt")
file_path01 = "./marutoonlinklist.txt"
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