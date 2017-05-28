from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='1111', db='moatoon', charset='utf8',autocommit=True)
curs = conn.cursor()

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser  = webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)

browser.get("http://webtoon.daum.net/")

now = datetime.now()
file_path = datetime.strftime(now, "./daumtoonlist01.txt")
file_path01 = "./daumtoonlinklist.txt"
data = ''
f = open(file_path, 'w', encoding='utf-8')
t = open(file_path01, 'w', encoding='utf-8')

# 페이지로딩 타임아웃
timeout = 10
try:
    graph = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='dayListTab']")))
except TimeoutException:
    print("Timed out")
    browser.quit()
daycount=1
while daycount <= 7:
    brw_path="//*[@id='dayListTab']/li["+str(daycount)+"]/a"
    browser.find_element_by_xpath(brw_path).click()
    time.sleep(1)
    browser.implicitly_wait(2)
    WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='cMain']/div[1]/div[1]")))
    dlc = len(browser.find_elements_by_xpath("//*[@id='dayList1']/li"))
    time.sleep(1)
    cnt=1
    while cnt <= dlc:
        thumb_path ="//*[@id='dayList1']/li["+str(cnt)+"]/a/img"
        thumb = browser.find_element_by_xpath(thumb_path)
        title_path = "//*[@id='dayList1']/li["+str(cnt)+"]/a/strong"
        title = browser.find_element_by_xpath(title_path)
        link_path = "//*[@id='dayList1']/li["+str(cnt)+"]/a"
        link = browser.find_element_by_xpath(link_path)
        author_path = "//*[@id='dayList1']/li["+str(cnt)+"]/span"
        author = browser.find_element_by_xpath(author_path)
        data = "[%4d번째 망가] 썸네일주소 : %s, 웹툰명 : %s, 웹툰주소 : %s, 작가 : %s\n" % \
               (cnt, thumb.get_attribute('src'), title.text, link.get_attribute('href'), author.text)
        tlist = "%s\n" % link.get_attribute('href')
        sql = '''insert into mainlist(site, title, author, thumb,main_link) values("daum","''' + title.text.strip() + '''","''' + author.text.strip() + '''","''' + thumb.get_attribute('src') + '''","''' + link.get_attribute('href') + '''")'''
        curs.execute(sql)
        f.write(data)
        t.write(tlist)
        cnt += 1
        print(str(cnt), str(thumb.get_attribute('src')), str(title.text), str(link.get_attribute('href')), str(author.text))

    dlc = len(browser.find_elements_by_xpath("//*[@id='dayList2']/li"))
    time.sleep(1)
    cnt = 1
    while cnt <= dlc :
        thumb_path = "//*[@id='dayList2']/li[" + str(cnt) + "]/a/img"
        thumb = browser.find_element_by_xpath(thumb_path)
        title_path = "//*[@id='dayList2']/li[" + str(cnt) + "]/a/strong"
        title = browser.find_element_by_xpath(title_path)
        link_path = "//*[@id='dayList2']/li[" + str(cnt) + "]/a"
        link = browser.find_element_by_xpath(link_path)
        author_path = "//*[@id='dayList2']/li[" + str(cnt) + "]/span"
        author = browser.find_element_by_xpath(author_path)
        data = "[%4d번째 망가] 썸네일주소 : %s, 웹툰명 : %s, 웹툰주소 : %s, 작가 : %s\n" % \
               (cnt, thumb.get_attribute('src'), title.text, link.get_attribute('href'), author.text)
        tlist = "%s\n" % link.get_attribute('href')
        sql = '''insert into mainlist(site, title, author, thumb,main_link) values("daum","''' + title.text.strip() + '''","''' + author.text.strip() + '''","''' + thumb.get_attribute(
            'src') + '''","''' + link.get_attribute('href') + '''")'''
        curs.execute(sql)
        f.write(data)
        t.write(tlist)
        cnt += 1
        print(str(cnt), str(thumb.get_attribute('src')), str(title.text), str(link.get_attribute('href')), str(author.text))
    daycount+=1

brw_path = "//*[@id='cMain']/div[1]/h3[2]/a"
browser.find_element_by_xpath(brw_path).click()
browser.implicitly_wait(2)
wangyulcount = 3
while wangyulcount <= 3:
    brw_path = "//*[@id='endListTab']/li[" + str(wangyulcount) + "]/a"
    browser.find_element_by_xpath(brw_path).click()
    time.sleep(1)
    browser.implicitly_wait(2)
    WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='cMain']/div[1]/div[2]")))
    dlc = len(browser.find_elements_by_xpath("//*[@id='endList']/li"))
    time.sleep(1)
    print(dlc)
    cnt = 1
    if wangyulcount == 2:
        print("유료")
    else:
        print("무료")
    while cnt <= dlc:
        thumb_path = "//*[@id='endList']/li[" + str(cnt) + "]/a/img"
        thumb = browser.find_element_by_xpath(thumb_path)
        title_path = "//*[@id='endList']/li[" + str(cnt) + "]/a/strong"
        title = browser.find_element_by_xpath(title_path)
        link_path = "//*[@id='endList']/li[" + str(cnt) + "]/a"
        link = browser.find_element_by_xpath(link_path)
        author_path = "//*[@id='endList']/li[" + str(cnt) + "]/span"
        author = browser.find_element_by_xpath(author_path)
        data = "[%4d번째 망가] 썸네일주소 : %s, 웹툰명 : %s, 웹툰주소 : %s, 작가 : %s\n" % \
               (cnt, thumb.get_attribute('src'), title.text, link.get_attribute('href'), author.text)
        tlist = "%s\n" % link.get_attribute('href')
        sql = '''insert into mainlist(site, title, author, thumb,main_link) values("daum","''' + title.text.strip() + '''","''' + author.text.strip() + '''","''' + thumb.get_attribute(
            'src') + '''","''' + link.get_attribute('href') + '''")'''
        curs.execute(sql)
        f.write(data)
        t.write(tlist)
        print(str(cnt), str(thumb.get_attribute('src')), str(title.text), str(link.get_attribute('href')), str(author.text))
        cnt += 1
    wangyulcount += 1

f.close()
t.close()
conn.close()