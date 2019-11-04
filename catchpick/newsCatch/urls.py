from django.urls import path
from . import views
app_name='newsCatch'
urlpatterns = [
    path('', views.home , name='home'),
]