from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

urlpatterns = [    
    path('food-items/', FoodItemCreate.as_view(), name='food-list'),
    path('labels/', FoodItemLabelCreate.as_view(), name='labels'),
    path('activities/', ActivityCreate.as_view(), name='activities'),
    path('daily-records/', DailyRecordCreate.as_view(), name='daily-records'),
    path('meal-records/', FoodItemRecordCreate.as_view(), name='meal-records'),
    path('activityrecords/', ActivityRecordCreate.as_view(), name='activityrecords'),
    
    
    path('food_item_record/', FoodItemRecordView.as_view(), name='food_item_record'),
    path('activity_record/', ActivityRecordView.as_view(), name='activity_record'),
    path('record_list/', RecordList.as_view(), name='record_list'),
]