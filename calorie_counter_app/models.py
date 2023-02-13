from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
from django.db.models.signals import post_save
from django.dispatch import receiver


class FoodItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    calories = models.IntegerField() 
    labels = models.ManyToManyField('FoodItemLabel')
    created = models.ForeignKey(User, on_delete=models.CASCADE)
    is_global = models.BooleanField(blank=True,null=True)
    approved_by_admin = models.BooleanField(blank=True,null=True)
    
class FoodItemLabel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    calories_burned_per_hour = models.IntegerField()
    created = models.ForeignKey(User, on_delete=models.CASCADE)
    is_global = models.BooleanField(blank=True,null=True)
    approved_by_admin = models.BooleanField(blank=True,null=True)

class DailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class FoodItemRecord(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    daily_record = models.ForeignKey(DailyRecord, on_delete=models.CASCADE)
    amount = models.FloatField()

class ActivityRecord(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    daily_record = models.ForeignKey(DailyRecord, on_delete=models.CASCADE)
    duration = models.FloatField()

