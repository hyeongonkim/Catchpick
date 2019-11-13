import requests
from bs4 import BeautifulSoup
import os, time
from selenium import webdriver

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catchpick.settings")
import django
django.setup()
# HTTP GET Request
from newsCatch.models import NewsTestData


# driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver')
driver_path = os.path.join('/Users/simonkim/PycharmProjects/KTISparse/catchpick/macchromedriver')
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome(driver_path, chrome_options=options)

driver.get('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=')
driver.find_element_by_id("_search_option_btn").click()

def getNews(company, keyword):
    global title1, link1, title2, link2, time1, time2
    driver.get('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + keyword)

    driver.find_element_by_id("news_popup").click()
    driver.find_element_by_id(company).click()
    driver.find_element_by_xpath("//*[@id='_nx_option_media']/div[2]/div[3]/button[1]").click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    newsTitle = soup.select('#sp_nws1 > dl > dt > a')
    newsTime = soup.select('#sp_nws1 > dl > dd.txt_inline')
    newsTitle2 = soup.select('#sp_nws2 > dl > dt > a')
    newsTime2 = soup.select('#sp_nws2 > dl > dd.txt_inline')
    for i in newsTitle:
        title1 = i.get('title')
        link1 = i.get('href')
    for l in newsTime:
        time1 = str(l).split('<span class="bar"></span>')[-3][1:-1]
    for j in newsTitle2:
        title2 = j.get('title')
        link2 = j.get('href')
    for m in newsTime2:
        time2 = str(m).split('<span class="bar"></span>')[-3][1:-1]

    forChkNews = [[title1, link1, time1],
                  [title2, link2, time2]]

    print(forChkNews)

companys = ['ca_1032', 'ca_1081', 'ca_1023', 'ca_1025', 'ca_1028', 'ca_1469'] #경향, 서울, 조선, 중앙, 한겨레, 한국

for i in companys:
    getNews(i, '전현무')

driver.quit()