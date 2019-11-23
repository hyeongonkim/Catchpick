from django.contrib import admin

# Register your models here.
from .models import TitleData, AccumulateData, NewsTestData, VerifiedData, EmailData
admin.site.register(TitleData)
admin.site.register(AccumulateData)
admin.site.register(NewsTestData)
admin.site.register(VerifiedData)
admin.site.register(EmailData)
