from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='1111', db='moatoon', charset='utf8',autocommit=True)
curs = conn.cursor()

driver = webdriver.Firefox()
driver.get("https://www.lezhin.com/ko/scheduled")

brw_path="//*[@id='comic-scheduled-btn-viewall']"
driver.find_element_by_xpath(brw_path).click()
driver.implicitly_wait(2)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

list = soup.select('div.comic-scheduled-comic')
ul = list[0].find('div').findAll('ul')

gourl = 'https://www.lezhin.com'

now = datetime.now()
file_path = datetime.strftime(now, "./lezhintoonlist01.txt")
file_path01 = "./lezhintoonlinklist.txt"
data = ''
f = open(file_path, 'w', encoding='utf-8')
t = open(file_path01, 'w', encoding='utf-8')

cnt = 1
for selectul in ul:

    if selectul == ul[0]:
        print("월")
    if selectul == ul[1]:
        print("화")
    if selectul == ul[2]:
        print("수")
    if selectul == ul[3]:
        print("목")
    if selectul == ul[4]:
        print("금")
    if selectul == ul[5]:
        print("토")
    if selectul == ul[6]:
        print("일")
    if selectul == ul[7]:
        print("열흘")
    if selectul == ul[8]:
        print("완결")

    for li in selectul:
        a = li.find('a')
        title = li.find('span')
        link = a['href']
        print(gourl + link, title.text)
        data = "[%4d번째 망가] 웹툰명 : %s, 웹툰주소 : %s\n" % \
               (cnt, title.text, gourl + link)
        tlist = "%s\n" % (gourl + link)
        # 썸네일과 작가가 필요한데 작가는 나중에 만화크롤러에서..
        sql = '''insert into mainlist(site,title) values("lezhin","''' + title.text.strip() +'''")'''
        curs.execute(sql)
        f.write(data)
        t.write(tlist)
        cnt += 1

f.close()
t.close()