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
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome(driver_path, chrome_options=options)

driver.get('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=')
driver.find_element_by_id("_search_option_btn").click()


def determineCategory(localCategory):
    ourCategory = ['정치', '경제', '사회', '국제', '스포츠', '문화']
    if localCategory in ourCategory:
        return localCategory
    elif localCategory == '연예':
        return '문화'
    elif localCategory == '문화·건강':
        return '문화'
    return '기타'


def CScategory(link):
    if (link.count('biz.chosun.com') >= 1):
        return '경제'
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(str(soup.select('#aside_sec_head_news_id > h3 > a')).split('">')[1][:-10])


def KHcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(str(soup.select('#container > div.art_side > div:nth-child(3) > div > div')).split('strong>')[1][:-2])


def CAcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(str(soup.select('body > div.doc > header > div.mh > div > h2 > a')).split('"_self">')[1][:-5])


def SUcategory(link):
    if(link.count('en.seoul.co.kr') >= 1):
        return '문화'
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(str(soup.select('body > div.wrap > div.top > div.top_menuBG > div > ul > li.sec_s > a')).split('"')[3].replace('최신', ''))


def HKRcategory(link):
    if(link.count('culture') >= 1):
        return '문화'
    elif (link.count('politics') >= 1):
        return '정치'
    elif (link.count('society') >= 1):
        return '사회'
    elif (link.count('economy') >= 1):
        return '경제'
    elif (link.count('international') >= 1):
        return '국제'
    elif (link.count('sports') >= 1):
        return '스포츠'
    return '기타'


def HKcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(str(soup.select('#HA > h2 > a')).split('">')[1][:-5])


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

# testData
# for i in companys:
#     getNews(i, '전현무')
#
# for i in companys:
#     getNews(i, '부동산')
#
# for i in companys:
#     getNews(i, '박찬주')
#
# print(KHcategory('http://news.khan.co.kr/kh_news/khan_art_view.html?artid=201911011401001&code=940301'))
# print(SUcategory('https://www.seoul.co.kr/news/newsView.php?id=20191111011011&wlog_tag3=naver'))
# print(CScategory('http://news.chosun.com/site/data/html_dir/2019/11/13/2019111300183.html?utm_source=naver&utm_medium=original&utm_campaign=news'))
# print(CAcategory('https://news.joins.com/article/23631213'))
# print(HKRcategory('http://www.hani.co.kr/arti/opinion/column/916770.html'))
# print(HKcategory('https://www.hankookilbo.com/News/Read/201911101899061149?did=NA&dtype=&dtypecode=&prnewsid='))

driver.quit()