from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()
router.register(r'food-items', FoodItemViewSet,basename='food-items')
router.register(r'labels', FoodItemLabelViewSet,basename='labels')
router.register(r'activities', ActivityViewSet,basename='activities')
router.register(r'daily-records', DailyRecordViewSet,basename='daily-records')
router.register(r'mealrecords', FoodItemRecordViewSet,basename='mealrecords')
router.register(r'activityrecords', ActivityRecordViewSet,basename='activityrecords')

urlpatterns = [
    path('', include(router.urls)),
    path('food_item_record/', FoodItemRecordView.as_view(), name='food_item_record'),
    path('activity_record/', ActivityRecordView.as_view(), name='activity_record'),
    path('record_list/', RecordList.as_view(), name='record_list'),
]