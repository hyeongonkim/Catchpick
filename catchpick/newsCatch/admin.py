from django.contrib import admin

# Register your models here.
from .models import TitleData, AccumulateData
admin.site.register(TitleData)
admin.site.register(AccumulateData)