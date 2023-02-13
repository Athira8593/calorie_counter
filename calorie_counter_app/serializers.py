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
        # fields = ('id', 'date', 'user', 'food_item', 'activities')
        fields = ('user',)

class FoodItemRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemRecord
        fields = ('id', 'food_item', 'amount','daily_record')

    def create(self, validated_data):
        food_item_id = validated_data.pop('food_item')
        food_item = FoodItem.objects.get(id=food_item_id)
        return FoodItemRecord.objects.create(food_item=food_item, **validated_data)









class ActivityRecordSerializer(serializers.ModelSerializer):
    # activity = ActivitySerializer()
    class Meta:
        model = ActivityRecord
        fields = ('id', 'activity', 'duration','daily_record')



