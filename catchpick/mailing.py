import requests
import os,django, time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catchpick.settings")

django.setup()

from newsCatch.models import VerifiedData, EmailData
from django.core.mail import EmailMessage


def daily_send():
     t = VerifiedData.objects.filter(time__gt=time.time() - 86400)  # 현재 서버시간 기준 24시간 이내 유효데이터만 t에 저
     for news in t:
          for data in EmailData.objects.all():#이메일 데이터를 불러옴
               email = EmailMessage(time.strftime('%Y년 %m월 %d일 catchpick뉴스입니다.', time.localtime(time.time())), news.news_KH_title,to =[data.email])
               # 이메일을 저장 순서대로 제목, 내용, 받는사람 으로 들어송
               email.send() #이메일 발송
             #현재 만드는 중이라서 타이틀 수 만큼 이메일이 발송됨 추후 수정할테니 신경쓰지말고 진행


if __name__=='__main__':
     daily_send()






