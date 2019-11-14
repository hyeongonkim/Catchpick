import requests
from bs4 import BeautifulSoup
import os, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catchpick.settings")
import django
django.setup()
# HTTP GET Request
from newsCatch.models import TitleData, AccumulateData, NewsTestData


def now_parse():
    TitleData.objects.all().delete()
    resp = requests.get('https://www.naver.com/')
    soup = BeautifulSoup(resp.text, 'html.parser')
    titles = soup.select('.ah_list .ah_k')
    return titles;


def accumulate_data():
    for i in range(1,21):
        for j in range(1,21):

    
    return 0;


if __name__=='__main__':
    titles = now_parse()
    cnt = 1
    # for title in titles:
    #     TitleData(title=title.get_text(),time= time.time(),nowRank=cnt).save()
    #     cnt+=1
    print(type(titles))





