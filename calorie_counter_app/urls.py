from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

urlpatterns = [
    path('add-fooditems/', FoodItemCreate.as_view(), name='add-fooditems'),
    path('list-fooditems/', FoodItemList.as_view(), name='list-fooditems'),
    path('add-labels/', FoodItemLabelCreate.as_view(), name='add-labels'),
    path('add-activities/', ActivityCreate.as_view(), name='add-activities'),
    path('list-activities/', ActivityList.as_view(), name='list-activities'),
    path('meals-records/', MealsRecordListCreate.as_view(), name='meals-records'),
    path('activity-records/', ActivityRecordListCreate.as_view(),name='activity-records'),
    
]
