import os, django, time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catchpick.settings")

django.setup()

from newsCatch.models import VerifiedData, EmailData
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def daily_send():
     todayNews = list(reversed(VerifiedData.objects.all().order_by('time')))

     if len(todayNews) != 0:
          for j in todayNews:
               j.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(j.time)))

          to = []

          for i in EmailData.objects.all():
               to.append(i.email)

          html_content = render_to_string('email.html', {'newsdata': todayNews})
          text_content = strip_tags(html_content)
          msg = EmailMultiAlternatives(time.strftime('%Y년 %m월 %d일 ~ ', time.localtime(time.time()-604800))+time.strftime('%Y년 %m월 %d일 주간 뉴스', time.localtime(time.time()))
, text_content, to=to)
          msg.attach_alternative(html_content, "text/html")
          msg.send()


if __name__=='__main__':
     daily_send()




