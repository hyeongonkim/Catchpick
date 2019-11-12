from django.db import models


# Create your models here.
class TitleData(models.Model):
    title = models.CharField(max_length=500)
    time = models.CharField(max_length=100,default = 0)
    def __str__(self):
        return self.title

class AccumulateData(models.Model):
    title = models.CharField(max_length=500)
    time = models.CharField(max_length=100, default = 0)
    def __str__(self):
        return self.title