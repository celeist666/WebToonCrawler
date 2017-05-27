from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='1111', db='moatoon', charset='utf8',autocommit=True)
curs = conn.cursor()

r = open('./lezhintoonlinklist.txt', 'r', encoding='UTF-8')
# r2 = open('./lezhintoonlist01.txt', 'r', encoding='UTF-8')
# t = open('./lezhintoonlist01.txt', 'w', encoding='utf-8')

ur = r.read()
urls = ur.split()

now = datetime.now()
file_path = datetime.strftime(now, "./lezhintoonlist.txt")
file_path01 = "./lezhintoonlist02.txt"
data = ''
f = open(file_path, 'w', encoding='utf-8')
t = open(file_path01, 'w', encoding='utf-8')

driver = webdriver.Firefox()
i = 0
for i in range(0, len(urls)):
    driver.get(urls[i])

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    imglist = soup.select('div.banner-wrap')
    img = imglist[0].find('img')['src']

    authorlist = soup.select('div.info')
    author = authorlist[0].find('p').find('a').text
    manganame = authorlist[0].find('h2').text
    print(author)
    print(img)

    list = soup.select('section.episode-main ul.episode-list li')
    cnt = 1
    for li in list:
        a = li.find('a')
        link = a['href']
        titlelist = a.findAll('div')

        hwa = titlelist[4].text
        title = titlelist[5].text
        date = titlelist[6].text

        print('https://www.lezhin.com/ko/comic/devildom/' + str(cnt), hwa, title, date)
        data = "[%4d번째 망가] 썸네일주소 : %s, 웹툰명 : %s, %s화, 제목 : %s, 날짜 : %s, 웹툰주소 : %s\n" % \
               (cnt, img, manganame, hwa, title, date, 'https://www.lezhin.com/ko/comic/devildom/' + str(cnt))
        tlist = "%s\n" % ('https://www.lezhin.com/ko/comic/devildom/' + str(cnt))
        sql = '''insert into toonlist(thumb,title,link,date) values("''' + img + '''","''' + hwa +"화 "+title + '''","''' +'https://www.lezhin.com/ko/comic/devildom/' + str(cnt) + '''","''' +date+'''")'''
        curs.execute(sql)
        f.write(data)
        t.write(tlist)
        cnt += 1

    i += 1

r.close()
f.close()
t.close()
conn.close()