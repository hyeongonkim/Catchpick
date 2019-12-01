from django.urls import path
from . import views
app_name='newsCatch'
urlpatterns = [
    path('', views.index , name='index'),
    path('politics/', views.politics , name='politics'),
    path('culture/', views.culture , name='culture'),
    path('society/', views.society , name='society'),
    path('economy/', views.economy , name='economy'),
    path('international/', views.international , name='international'),
    path('sports/', views.sports , name='sports'),
    path('etc/', views.etc , name='etc'),
    path('about/', views.about, name='about'),
    path('subscription/', views.subscription, name='subscription'),
    path('unsubscription/', views.unsubscription, name='unsubscription'),
    path('errorsubs/', views.errorsubs, name='errorsubs'),
    path('errorunsubs/', views.errorunsubs, name='errorunsubs'),
]
