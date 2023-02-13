from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class FoodItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    calories = models.IntegerField()
    labels = models.ManyToManyField('FoodItemLabel')
    created = models.ForeignKey(User, on_delete=models.CASCADE)
    is_global = models.BooleanField(blank=True, null=True)
    approved_by_admin = models.BooleanField(blank=True, null=True)


class FoodItemLabel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    calories_burned_per_hour = models.IntegerField()
    created = models.ForeignKey(User, on_delete=models.CASCADE)
    is_global = models.BooleanField(blank=True, null=True)
    approved_by_admin = models.BooleanField(blank=True, null=True)


class MealsRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    amount_consumed = models.IntegerField()
    total_calorie_consumed = models.IntegerField(blank=True, null=True)

    
class ActivityRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    duration = models.FloatField()
    total_calorie_burned = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
class DailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    consumption = models.ForeignKey(MealsRecord, on_delete=models.CASCADE)
    burn_out = models.ForeignKey(ActivityRecord, on_delete=models.CASCADE)

