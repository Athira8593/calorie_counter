from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import FoodItem, FoodItemLabel, Activity, DailyRecord, ActivityRecord, MealsRecord
from .serializers import *
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import login
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear


class FoodItemCreate(generics.CreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created=self.request.user)
        print(self.request.user)
        if self.request.user.is_staff:
            serializer.save(is_global=True, approved_by_admin=True)
        else:
            serializer.save(is_global=False, approved_by_admin=False)


class FoodItemList(generics.ListAPIView):
    queryset = FoodItem.objects.filter(approved_by_admin=True)
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]


class FoodItemLabelCreate(generics.ListCreateAPIView):
    queryset = FoodItemLabel.objects.all()
    serializer_class = FoodItemLabelSerializer
    permission_classes = [IsAuthenticated]


class ActivityCreate(generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created=self.request.user)

        if self.request.user.is_staff:
            serializer.save(is_global=True, approved_by_admin=True)
        else:
            serializer.save(is_global=False, approved_by_admin=False)


class ActivityList(generics.ListAPIView):
    queryset = Activity.objects.filter(approved_by_admin=True)
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]


class MealsRecordListCreate(generics.ListCreateAPIView):
    queryset = MealsRecord.objects.all()
    serializer_class = MealsRecordSerializer
    permission_classes = [IsAuthenticated]

        
    def perform_create(self, serializer): 
        amount_consumed = int(self.request.data.get('amount_consumed'))
        food_item_id = int(self.request.data.get('food_item'))
        food_item = FoodItem.objects.get(id=food_item_id)
        total_calorie_consumed = food_item.calories*amount_consumed
        serializer.save(total_calorie_consumed=total_calorie_consumed, user=self.request.user)
        

class ActivityRecordListCreate(generics.ListCreateAPIView):
    queryset = ActivityRecord.objects.all()
    serializer_class = ActivityRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): 
        duration = int(self.request.data.get('duration'))
        activity_id = int(self.request.data.get('activity'))
        activity = Activity.objects.get(id=activity_id)
        total_calorie_burned = (activity.calories_burned_per_hour*duration)
        serializer.save(total_calorie_burned=total_calorie_burned, user=self.request.user)



