from django.shortcuts import render, redirect
from .forms import EmailForm
from .models import EmailData
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def politics(request):
    return render(request,'newsCatch/politics.html')
def culture(request):
    return render(request,'newsCatch/culture.html')
def society(request):
    return render(request,'newsCatch/society.html')
def economy(request):
    return render(request,'newsCatch/economy.html')
def international(request):
    return render(request,'newsCatch/international.html')
def sports(request):
    return render(request,'newsCatch/sports.html')
def etc(request):
    return render(request,'newsCatch/etc.html')

def about(request):
    return render(request,'newsCatch/about.html')

def subscription(request): # 구독 페이지 처리
    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid(): #폼이 유효하면 이메일 저장
            if EmailData.objects.filter(email=request.POST.get('email')).count() ==0: #EmailData DB에 입력된 이메일이 없다면 이메일 저장
                subscription = form.save()
                return redirect('newsCatch:politics')
            else:  #EmailData DB에 이미 있는 이메일이면 에러페이지로 이동
                return render(request, 'newsCatch/sub_emailError.html')
        else: #이메일 형석 예외처리
            return render(request, 'newsCatch/sub_emailError.html')

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
                return render(request, 'newsCatch/unsub_emailError.html')
        except ObjectDoesNotExist: #삭제하려는 이메일이 EmailData DB에 없다면 에러페이지 출력
            return render(request, 'newsCatch/emailDoseNotExist.html')


    else:
        form = EmailForm()
        return render(request, 'newsCatch/unsubscription.html', {'form': form})

