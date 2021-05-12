from django.db import models


# Create your models here.
class useravatar(models.Model):
    image = models.FileField(upload_to='static/user-avatar/')
