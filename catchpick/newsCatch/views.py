from django.shortcuts import render, redirect
from .forms import EmailForm
from .models import EmailData, VerifiedData
from django.core.exceptions import ObjectDoesNotExist
import time
# Create your views here.


def politics(request):
    all_news_data = list(reversed(VerifiedData.objects.all().order_by('time')))
    for j in all_news_data:
        j.title = j.title + ', '
    all_news_data[len(all_news_data) - 1].title = all_news_data[len(all_news_data) - 1].title[:-2]
    news_data = VerifiedData.objects.filter(category="정치")
    for i in news_data:
        i.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(i.time)))
    return render(request, 'newsCatch/politics.html', {'all_news_data': all_news_data, 'news_data': news_data})
def culture(request):
    all_news_data = list(reversed(VerifiedData.objects.all().order_by('time')))
    for j in all_news_data:
        j.title = j.title + ', '
    all_news_data[len(all_news_data) - 1].title = all_news_data[len(all_news_data) - 1].title[:-2]
    news_data = VerifiedData.objects.filter(category="문화")
    for i in news_data:
        i.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(i.time)))
    return render(request, 'newsCatch/culture.html', {'all_news_data': all_news_data, 'news_data': news_data})
def society(request):
    all_news_data = list(reversed(VerifiedData.objects.all().order_by('time')))
    for j in all_news_data:
        j.title = j.title + ', '
    all_news_data[len(all_news_data) - 1].title = all_news_data[len(all_news_data) - 1].title[:-2]
    news_data = VerifiedData.objects.filter(category="사회")
    for i in news_data:
        i.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(i.time)))
    return render(request, 'newsCatch/society.html', {'all_news_data': all_news_data, 'news_data': news_data})
def economy(request):
    all_news_data = list(reversed(VerifiedData.objects.all().order_by('time')))
    for j in all_news_data:
        j.title = j.title + ', '
    all_news_data[len(all_news_data) - 1].title = all_news_data[len(all_news_data) - 1].title[:-2]
    news_data = VerifiedData.objects.filter(category="경제")
    for i in news_data:
        i.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(i.time)))
    return render(request, 'newsCatch/economy.html', {'all_news_data': all_news_data, 'news_data': news_data})
def international(request):
    all_news_data = list(reversed(VerifiedData.objects.all().order_by('time')))
    for j in all_news_data:
        j.title = j.title + ', '
    all_news_data[len(all_news_data) - 1].title = all_news_data[len(all_news_data) - 1].title[:-2]
    news_data = VerifiedData.objects.filter(category="국제")
    for i in news_data:
        i.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(i.time)))
    return render(request, 'newsCatch/international.html', {'all_news_data': all_news_data, 'news_data': news_data})
def sports(request):
    all_news_data = list(reversed(VerifiedData.objects.all().order_by('time')))
    for j in all_news_data:
        j.title = j.title + ', '
    all_news_data[len(all_news_data) - 1].title = all_news_data[len(all_news_data) - 1].title[:-2]
    news_data = VerifiedData.objects.filter(category="스포츠")
    for i in news_data:
        i.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(i.time)))
    return render(request, 'newsCatch/sports.html', {'all_news_data': all_news_data, 'news_data': news_data})
def etc(request):
    all_news_data = list(reversed(VerifiedData.objects.all().order_by('time')))
    for j in all_news_data:
        j.title = j.title + ', '
    all_news_data[len(all_news_data) - 1].title = all_news_data[len(all_news_data) - 1].title[:-2]
    news_data = VerifiedData.objects.filter(category="기타")
    for i in news_data:
        i.time = time.strftime('%m월 %d일 %H:%M ~', time.localtime(float(i.time)))
    return render(request, 'newsCatch/etc.html', {'all_news_data': all_news_data, 'news_data': news_data})

def about(request):
    return render(request,'newsCatch/about.html')

def subscription(request): # 구독 페이지 처리
    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid(): #폼이 유효하면 이메일 저장
            if EmailData.objects.filter(email=request.POST.get('email')).count() == 0: #EmailData DB에 입력된 이메일이 없다면 이메일 저장
                subscription = form.save()
                return redirect('newsCatch:politics')
            else:  #EmailData DB에 이미 있는 이메일이면 에러페이지로 이동
                return redirect('newsCatch:errorsubs')
        else: #이메일 형석 예외처리
            return redirect('newsCatch:errorsubs')
    else:
        form = EmailForm()
        return render(request, 'newsCatch/subscription.html', {'form': form})
def unsubscription(request): #구독취소 페이지 처리
    if request.method == "POST":

        form = EmailForm(request.POST)
        del_email = request.POST.get('email')
        try: #삭제하려는 이메일이 EmailData DB에 있으면 삭제
            if form.is_valid() and EmailData.objects.get(email=del_email):
                unsubscription = EmailData.objects.get(email=del_email)
                unsubscription.delete()
                return redirect('newsCatch:politics')
            else: #이메일 형식 예외처리
                return redirect('newsCatch:errorunsubs')
        except ObjectDoesNotExist: #삭제하려는 이메일이 EmailData DB에 없다면 에러페이지 출력
            return redirect('newsCatch:errorunsubs')
    else:
        form = EmailForm()
        return render(request, 'newsCatch/unsubscription.html', {'form': form})

def errorsubs(request):
    return render(request, 'newsCatch/sub_emailError.html')

def errorunsubs(request):
    return render(request, 'newsCatch/unsub_emailError.html')