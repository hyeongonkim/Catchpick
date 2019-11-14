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
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
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
    if 'biz.chosun.com' in link:
        return '경제'
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(str(soup.select('#aside_sec_head_news_id > h3 > a')).split('">')[1][:-10])


def KHcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(
        str(soup.select('#header > div.logo_area > div.sec_title > a')).split(');">')[1][:-5])


def CAcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(
        str(soup.select('body > div.doc > header > div.mh > div > h2 > a')).split('"_self">')[1][:-5])


def SUcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    chkEn = str(soup.select('#en_navi > center > div > p > a > img'))
    if '서울en' in chkEn:
        return '문화'
    return determineCategory(
        str(soup.select('body > div.wrap > div.top > div.top_menuBG > div > ul')).split('<a href="')[3].split('"')[2].replace(
            '최신', ''))


def HKRcategory(link):
    if 'culture' in link:
        return '문화'
    elif 'politics' in link:
        return '정치'
    elif 'society' in link:
        return '사회'
    elif 'economy' in link:
        return '경제'
    elif 'international' in link:
        return '국제'
    elif 'sports' in link:
        return '스포츠'
    return '기타'


def HKcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    chkEn = str(soup.select('body > header > div.MmenuCon > div > h1 > a > img'))
    if 'logo_enter' in chkEn:
        return '문화'
    return determineCategory(str(soup.select('#content > article > div.content-body > div > section > h3 > span'))[7:-8])


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

    if keyword in title2 and keyword not in title1:
        return [title2, link2, time2]
    if ('분 전' in time2 or '시간 전' in time2) and ('분 전' not in time1 and '시간 전' not in time1):
        return [title2, link2, time2]
    if '[전문]' in title2 or '[종합]' in title2:
        if '분 전' in time2 or '시간 전' in time2:
            return [title2, link2, time2]
    if '[포토]' in title1:
        if '분 전' in time2 or '시간 전' in time2:
            return [title2, link2, time2]
    return [title1, link1, time1]


companys = ['ca_1032', 'ca_1081', 'ca_1023', 'ca_1025', 'ca_1028', 'ca_1469']  # 경향, 서울, 조선, 중앙, 한겨레, 한국

# for i in NewsTestData.objects.all():
#     title = i.title
#     news = []
#     newsCnt = 0
#     companyCnt = 0
#     for j in companys:
#         nowData = getNews(j, title)
#         if title not in nowData[0] or ('분 전' not in nowData[2] and '시간 전' not in nowData[2]):
#             companyCnt = companyCnt + 1
#             continue
#         if companyCnt == 0:
#             nowData.append(KHcategory(nowData[1]))
#         elif companyCnt == 1:
#             nowData.append(SUcategory(nowData[1]))
#         elif companyCnt == 2:
#             nowData.append(CScategory(nowData[1]))
#         elif companyCnt == 3:
#             nowData.append(CAcategory(nowData[1]))
#         elif companyCnt == 4:
#             nowData.append(HKRcategory(nowData[1]))
#         elif companyCnt == 5:
#             nowData.append(HKcategory(nowData[1]))
#         news.append(nowData)
#         newsCnt = newsCnt + 1
#         companyCnt = companyCnt + 1
#     if newsCnt >= 4:
#         print(news) # 모델에 데이터 삽입


# testData
testDatas = ['흑사병']
for i in testDatas:
    title = i
    news = []
    newsCnt = 0
    companyCnt = 0
    for j in companys:
        nowData = getNews(j, title)
        if title not in nowData[0] or ('분 전' not in nowData[2] and '시간 전' not in nowData[2]):
            companyCnt = companyCnt + 1
            continue
        if companyCnt == 0:
            nowData.append(KHcategory(nowData[1]))
            nowData.append('경향')
        elif companyCnt == 1:
            nowData.append(SUcategory(nowData[1]))
            nowData.append('서울')
        elif companyCnt == 2:
            nowData.append(CScategory(nowData[1]))
            nowData.append('조선')
        elif companyCnt == 3:
            nowData.append(CAcategory(nowData[1]))
            nowData.append('중앙')
        elif companyCnt == 4:
            nowData.append(HKRcategory(nowData[1]))
            nowData.append('한겨레')
        elif companyCnt == 5:
            nowData.append(HKcategory(nowData[1]))
            nowData.append('한국')
        news.append(nowData)
        newsCnt = newsCnt + 1
        companyCnt = companyCnt + 1
    if newsCnt >= 4:
        print(news)  # 모델에 데이터 삽입

driver.quit()
