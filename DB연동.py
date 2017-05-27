import pymysql

conn = pymysql.connect(host='localhost', user='root', password='1111', db='moatoon', charset='utf8')

curs = conn.cursor()

title = 'a'
author = 'b'
thumb = 'c'
sql = "insert into mainlist(site, title, author, thumb) values('daum','"+title+"','"+author+"','"+thumb+"')"

curs.execute(sql)

curs.execute(sql)
rows = curs.fetchall()
print(rows)

conn.close()