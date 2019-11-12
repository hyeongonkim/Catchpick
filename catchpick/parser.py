import requests
from bs4 import BeautifulSoup
import os, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catchpick.settings")
import django
django.setup()
# HTTP GET Request
from newsCatch.models import TitleData




resp = requests.get('https://www.naver.com/')
soup = BeautifulSoup(resp.text, 'html.parser')
titles = soup.select('.ah_list .ah_k')

for title in titles:
    TitleData(title=title.get_text(),time= time.time()).save()




