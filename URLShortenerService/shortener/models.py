from django.db import models

# Create your models here.
class URL(models.Model):
    uid = models.PositiveBigIntegerField(primary_key=True)
    long_url= models.CharField(max_length=2048)
    short_url = models.CharField(max_length=20, unique=True)
    