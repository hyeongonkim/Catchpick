import requests
from bs4 import BeautifulSoup
import os, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catchpick.settings")
import django
django.setup()
# HTTP GET Request
from newsCatch.models import TitleData, AccumulateData, NewsTestData



def now_parse(): # 최신 검색어를 파싱합니다.
    TitleData.objects.all().delete()
    resp = requests.get('https://www.naver.com/')
    soup = BeautifulSoup(resp.text, 'html.parser')
    titles = soup.select('.ah_list .ah_k')
    return titles; # 최신 검색어 목록을 리스트 형태로 리턴합니다.


def accumulate_data(now_list): # 데이터를 축적하는 함수입니다. 현재 파싱된 데이터 리스트를 인자로 받습니다.
    for i in range(0,20):
        Now=TitleData.objects.get(title=now_list[i].get_text())
        try:
            Accumulate = AccumulateData.objects.get(title=now_list[i].get_text())
            if(int(Now.nowRank) < int(Accumulate.maxRank)): # 현재 파싱데이터의 랭킹과 누적된 데이터의 랭킹을 비교합니다.

                               # 현재 파싱데이터의 순위가 더 높으면 검색어 순위를 업데이트 합니다.
                Accumulate.maxRank=Now.nowRank
                Accumulate.save()
                if Accumulate.toNewsTest == True: #이미 NewsTestData로 넘겨준 데이터의 순위가 바뀐 경우 NewsTestData에 다시 저장합니다.
                    update_Rank = NewsTestData(title=Accumulate.title, time=Accumulate.time, maxRank=Accumulate.maxRank)
                    update_Rank.save()


        except AccumulateData.DoesNotExist: # 현재 파싱데이터가 누적된 데이터에 존재하지 않으면 새로운 누적데이터를 만듭니다.
            New = AccumulateData(title=Now.title,time=Now.time,maxRank=Now.nowRank)
            New.save()
        if ((AccumulateData.objects.get(title=now_list[i].get_text()).toNewsTest == False) and ((float(Now.time)-float(AccumulateData.objects.get(title=now_list[i].get_text()).time)) > 10800)):
            pass_Accumulate = AccumulateData.objects.get(title=now_list[i].get_text())
            pass_Accumulate.toNewsTest = True
            pass_Accumulate.save()
            NewsTest = NewsTestData(title=pass_Accumulate.title, time=pass_Accumulate.time, maxRank=pass_Accumulate.maxRank)
            NewsTest.save()











if __name__=='__main__':
    titles = now_parse() # 현재 검색어를 파싱합니다.
    cnt = 1
    for title in titles: # 현재 파싱데이터의 타이틀,시간,순위를 저장합니다.
        TitleData(title=title.get_text(),time= time.time(),nowRank=cnt).save()
        cnt+=1
    accumulate_data(titles) # 누적데이터와 현재데이터를 비교합니다.





