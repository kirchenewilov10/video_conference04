from django.db import models


# Create your models here.
class software(models.Model):
    filepath = models.FileField(upload_to='static/softwares/')
