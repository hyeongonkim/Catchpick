from django.db import models


# Create your models here.
class TitleData(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=100, default=0)
    nowRank = models.CharField(max_length=100, default=21)

    def __str__(self):
        return self.title

class AccumulateData(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=100, default=0)
    maxRank = models.CharField(max_length=100, default=21)
    toNewsTest = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class NewsTestData(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=100, default=0)
    maxRank = models.CharField(max_length=100, default=21)

    def __str__(self):
        return self.title

class VerifiedData(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=100, default=0)
    maxRank = models.CharField(max_length=100, default=21)
    category = models.CharField(max_length=100)
    news_KH_title = models.CharField(max_length=100)
    news_KH_link = models.CharField(max_length=100)
    news_HKR_title = models.CharField(max_length=100)
    news_HKR_link = models.CharField(max_length=100)
    news_CS_title = models.CharField(max_length=100)
    news_CS_link = models.CharField(max_length=100)
    news_CA_title = models.CharField(max_length=100)
    news_CA_link = models.CharField(max_length=100)
    news_SU_title = models.CharField(max_length=100)
    news_SU_link = models.CharField(max_length=100)
    news_HK_title = models.CharField(max_length=100)
    news_HK_link = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class EmailData(models.Model):
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email