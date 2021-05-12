from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class contactus(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)

class devicetypes(models.Model):
    name = models.CharField(max_length=255, blank=True)

class menu_tree(models.Model):
    parent_id = models.IntegerField(default=0)
    has_child = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    level = models.IntegerField(default=0)

class off_days(models.Model):
    userid = models.IntegerField(default=0, blank=True)
    off_day = models.DateField(blank=True, null=True)

class orders(models.Model):
    userid = models.IntegerField(default=0, blank=True)
    service_id = models.IntegerField(default=0, blank=True)
    category_type = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0)
    pay_status = models.IntegerField(default=0)
    service_status = models.IntegerField(default=0)
    # 0: created, 1: accepted, 2: cancelled by customer, 3: finished, 4: rejected by admin
    paid_price = models.FloatField(default=0)
    date_created = models.DateTimeField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True)
    review = models.TextField(blank=True)
    score = models.FloatField(default=0)
    user_response = models.TextField(blank=True)
    booked = models.IntegerField(default=0)
    date_booked = models.DateTimeField(blank=True, null=True)

class oss(models.Model):
    name = models.CharField(max_length=255, blank=True)

class prices(models.Model):
    service_id = models.IntegerField(blank=True, default=0)
    item_comb = models.CharField(max_length=255, blank=True)
    price = models.FloatField(default=0, blank=True)

class Room(models.Model):
    users = models.TextField(blank=True)
    source = models.CharField(max_length=10, default='Website')
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    track = models.TextField(blank=True, editable=False)
    status = models.CharField(max_length=10, default='Active')

class services(models.Model):
    level = models.IntegerField(default=0)
    parentid = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    index = models.CharField(max_length=255, blank=True)

class softwares(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

class transactions(models.Model):
    userid = models.IntegerField(blank=True)
    deposit_date = models.DateTimeField(blank=True)
    mode = models.IntegerField(blank=True, default=0)
    amount = models.FloatField(blank=True, default=0)
    tracking_number = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)


class tbl_user(AbstractUser):
    phone = models.CharField(max_length=255, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=255, blank=True)
    parent_id = models.IntegerField(default=0)
    permission = models.CharField(max_length=255, blank=True)
    image_path = models.TextField(blank=True)
    deleted = models.IntegerField(default=0)
    spent_money = models.FloatField(default=0)
    current_money = models.FloatField(default=0)
    service_usable = models.IntegerField(default=0)