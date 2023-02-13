from rest_framework import serializers
from .models import FoodItem, FoodItemLabel, Activity, DailyRecord, FoodItemRecord, ActivityRecord
from django.contrib.auth.models import User


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('id', 'name', 'calories', 'labels')

class FoodItemLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemLabel
        fields = ('id', 'name')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'calories_burned_per_hour')

class DailyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecord
        fields = ('id', 'date', 'user', 'food_item', 'activities')

class FoodItemRecordSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()
    class Meta:
        model = FoodItemRecord
        fields = ('id', 'food_item', 'amount','daily_record')

class ActivityRecordSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    class Meta:
        model = ActivityRecord
        fields = ('id', 'activity', 'duration','daily_record')



