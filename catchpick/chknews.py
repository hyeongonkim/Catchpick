from bs4 import BeautifulSoup
import os, time
from selenium import webdriver
from collections import Counter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catchpick.settings")
import django

django.setup()
# HTTP GET Request
from newsCatch.models import NewsTestData
from newsCatch.models import VerifiedData


def determineCategory(localCategory):
    ourCategory = ['정치', '경제', '사회', '국제', '스포츠', '문화']
    if localCategory in ourCategory:
        return localCategory
    elif localCategory == '연예':
        return '문화'
    elif localCategory == '문화·건강':
        return '문화'
    elif localCategory == '생활·문화':
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


def SBScategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(
        str(soup.select('#container > div.w_inner > div.w_top_cs > ul > li.cate03 > a')).split('">')[1][:-5])


def YTNcategory(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return determineCategory(
        str(soup.select('#zone1 > div.article_info > div > b'))[4:-5])


def getNews(company, keyword):
    global title1, link1, title2, link2, time1, time2
    driver.get('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + keyword)

    driver.find_element_by_id("news_popup").click()
    driver.find_element_by_id(company).click()
    driver.find_element_by_xpath("//*[@id='_nx_option_media']/div[2]/div[3]/button[1]").click()
    driver.find_element_by_xpath("// *[ @ id = 'snb'] / div / ul / li[2] / a").click()
    driver.find_element_by_xpath("//*[@id='_nx_option_date']/div[1]/ul[1]/li[2]/a").click()


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    newsTitle = soup.select('#sp_nws1 > dl > dt > a')
    newsTime = soup.select('#sp_nws1 > dl > dd.txt_inline')
    newsTitle2 = soup.select('#sp_nws2 > dl > dt > a')
    newsTime2 = soup.select('#sp_nws2 > dl > dd.txt_inline')

    if len(newsTitle) == 0:
        return ['empty', 'empty', 'empty']

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

    if len(newsTitle2) == 0:
        return [title1, link1, time1]

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


driver_path = os.path.join(os.getcwd() + '/chromedriver')
# driver_path = os.path.join('/Users/simonkim/PycharmProjects/KTISparse/catchpick/macchromedriver')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('no-sandbox')
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome(driver_path, chrome_options=options)

try:
    driver.get('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=')
    driver.find_element_by_id("_search_option_btn").click()


    companys = ['ca_1032', 'ca_1023', 'ca_1025', 'ca_1028', 'ca_1056', 'ca_1214', 'ca_1055',
                'ca_1052']  # 경향, 조선, 중앙, 한겨레, KBS, MBC, SBS, YTN

    nowTime = time.time()
    #기존데이터 리프레시
    for i in VerifiedData.objects.all():
        title = i.title
        if nowTime - float(i.time) >= 604800:
            i.delete()
            continue
        news = []
        newsCnt = 0
        companyCnt = 0
        for j in companys:
            nowData = getNews(j, title)
            if '분 전' not in nowData[2] and '시간 전' not in nowData[2]:
                companyCnt = companyCnt + 1
                continue
            testList = title.split()
            chkTitleTest = False
            for tempkey in testList:
                if tempkey in nowData[0]:
                    chkTitleTest = True
            if not chkTitleTest:
                companyCnt = companyCnt + 1
                continue
            if companyCnt == 0:
                nowData.append('경향')
            elif companyCnt == 1:
                nowData.append('조선')
            elif companyCnt == 2:
                nowData.append('중앙')
            elif companyCnt == 3:
                nowData.append('한겨레')
            elif companyCnt == 4:
                nowData.append('KBS')
            elif companyCnt == 5:
                nowData.append('MBC')
            elif companyCnt == 6:
                nowData.append('SBS')
            elif companyCnt == 7:
                nowData.append('YTN')
            news.append(nowData)
            newsCnt = newsCnt + 1
            companyCnt = companyCnt + 1

        verify = [i.news_KH_title, i.news_KH_link, i.news_HKR_title, i.news_HKR_link, i.news_CS_title, i.news_CS_link,
                i.news_CA_title, i.news_CA_link, i.news_KBS_title, i.news_KBS_link, i.news_MBC_title, i.news_MBC_link,
                i.news_SBS_title, i.news_SBS_link, i.news_YTN_title, i.news_YTN_link]
        for k in news:
            if '경향' == k[3]:
                verify[0] = k[0]
                verify[1] = k[1]
            elif '조선' == k[3]:
                verify[4] = k[0]
                verify[5] = k[1]
            elif '중앙' == k[3]:
                verify[6] = k[0]
                verify[7] = k[1]
            elif '한겨레' == k[3]:
                verify[2] = k[0]
                verify[3] = k[1]
            elif 'SBS' == k[3]:
                verify[12] = k[0]
                verify[13] = k[1]
            elif 'YTN' == k[3]:
                verify[14] = k[0]
                verify[15] = k[1]
            elif 'MBC' == k[3]:
                verify[10] = k[0]
                verify[11] = k[1]
            elif 'KBS' == k[3]:
                verify[8] = k[0]
                verify[9] = k[1]
        tempTitle = i.title
        tempTime = i.time
        tempMaxRank = i.maxRank
        tempCategory = i.category
        i.delete()
        VerifiedData(title=tempTitle, time=tempTime, maxRank=tempMaxRank, category=tempCategory,
                    news_KH_title=verify[0],
                    news_KH_link=verify[1], news_HKR_title=verify[2], news_HKR_link=verify[3], news_CS_title=verify[4],
                    news_CS_link=verify[5], news_CA_title=verify[6], news_CA_link=verify[7], news_KBS_title=verify[8],
                    news_KBS_link=verify[9], news_MBC_title=verify[10], news_MBC_link=verify[11],
                    news_SBS_title=verify[12], news_SBS_link=verify[13], news_YTN_title=verify[14],
                    news_YTN_link=verify[15]).save()

    # 신규데이터 검사
    for i in NewsTestData.objects.all():
        title = i.title
        try:
            rankChange = VerifiedData.objects.get(title=title)
            rankChange.maxRank = i.maxRank
            rankChange.save()
        except VerifiedData.DoesNotExist:
            testAlready = title.split()
            chkTestAlready = False
            for splited in testAlready:
                try:
                    test = VerifiedData.objects.get(title=splited)
                    chkTestAlready = True
                    break
                except VerifiedData.DoesNotExist:
                    continue
            if chkTestAlready:
                continue
            news = []
            newsCnt = 0
            companyCnt = 0
            for j in companys:
                nowData = getNews(j, title)
                if '분 전' not in nowData[2] and '시간 전' not in nowData[2]:
                    companyCnt = companyCnt + 1
                    continue
                testList = title.split()
                chkTitleTest = False
                for tempkey in testList:
                    if tempkey in nowData[0]:
                        chkTitleTest = True
                if not chkTitleTest:
                    companyCnt = companyCnt + 1
                    continue
                if companyCnt == 0:
                    nowData.append('경향')
                elif companyCnt == 1:
                    nowData.append('조선')
                elif companyCnt == 2:
                    nowData.append('중앙')
                elif companyCnt == 3:
                    nowData.append('한겨레')
                elif companyCnt == 4:
                    nowData.append('KBS')
                elif companyCnt == 5:
                    nowData.append('MBC')
                elif companyCnt == 6:
                    nowData.append('SBS')
                elif companyCnt == 7:
                    nowData.append('YTN')
                news.append(nowData)
                newsCnt = newsCnt + 1
                companyCnt = companyCnt + 1
            if newsCnt >= 3:
                category = []
                verify = []
                for cnt in range(16):
                    verify.append('empty')
                for k in news:
                    if '경향' == k[3]:
                        category.append(KHcategory(k[1]))
                        verify[0] = k[0]
                        verify[1] = k[1]
                    elif '조선' == k[3]:
                        category.append(CScategory(k[1]))
                        verify[4] = k[0]
                        verify[5] = k[1]
                    elif '중앙' == k[3]:
                        category.append(CAcategory(k[1]))
                        verify[6] = k[0]
                        verify[7] = k[1]
                    elif '한겨레' == k[3]:
                        category.append(HKRcategory(k[1]))
                        verify[2] = k[0]
                        verify[3] = k[1]
                    elif 'SBS' == k[3]:
                        category.append(SBScategory(k[1]))
                        verify[12] = k[0]
                        verify[13] = k[1]
                    elif 'YTN' == k[3]:
                        category.append(YTNcategory(k[1]))
                        verify[14] = k[0]
                        verify[15] = k[1]
                    elif 'MBC' == k[3]:
                        verify[10] = k[0]
                        verify[11] = k[1]
                    elif 'KBS' == k[3]:
                        verify[8] = k[0]
                        verify[9] = k[1]
                cnt = Counter(category)
                mostCategory = cnt.most_common(1)[0][0]
                VerifiedData(title=i.title, time=i.time, maxRank=i.maxRank, category=mostCategory, news_KH_title=verify[0],
                            news_KH_link=verify[1], news_HKR_title=verify[2], news_HKR_link=verify[3],
                            news_CS_title=verify[4],
                            news_CS_link=verify[5], news_CA_title=verify[6], news_CA_link=verify[7],
                            news_KBS_title=verify[8],
                            news_KBS_link=verify[9], news_MBC_title=verify[10], news_MBC_link=verify[11],
                            news_SBS_title=verify[12], news_SBS_link=verify[13], news_YTN_title=verify[14],
                            news_YTN_link=verify[15]).save()
        i.delete()
except:
    driver.quit()
driver.quit()
