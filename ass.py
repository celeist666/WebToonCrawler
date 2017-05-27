import requests
from bs4 import BeautifulSoup
import datetime

# date = datetime.date.today()
# new = date+datetime.timedelta(days=7)
# start_date = "10/10/11"
# date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")
#
# end_date = date_1 + datetime.timedelta(days=6)
# new.strftime('%Y/%m/%d')
date = "7일 후 무료"
date2=date.split("일 후 무료")
date3 = "1"
date4=date3.split("일 후 무료")
print(date2)
print(date4)