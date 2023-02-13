from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import FoodItem, FoodItemLabel, Activity, DailyRecord, FoodItemRecord, ActivityRecord
from .serializers import *
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate

# from django.http import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import login
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear



class FoodItemCreate(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(created=self.request.user)
        if self.request.user.is_staff:
            serializer.save(is_global = True,approved_by_admin = True)
        else:
            serializer.save(is_global = False,approved_by_admin = False)
    
class FoodItemLabelCreate(generics.ListCreateAPIView):
    queryset = FoodItemLabel.objects.all()
    serializer_class = FoodItemLabelSerializer
    permission_classes = [IsAdminUser] 
    
class ActivityCreate(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(created=self.request.user)
        
        if self.request.user.is_staff:
            serializer.save(is_global = True,approved_by_admin = True)
        else:
            serializer.save(is_global = False,approved_by_admin = False)
            
class DailyRecordCreate(generics.ListCreateAPIView):
    queryset = DailyRecord.objects.all()
    serializer_class = DailyRecordSerializer
    permission_classes = [IsAuthenticated]
    
    
    
# class FoodItemRecordCreate(generics.ListCreateAPIView):
#     queryset = FoodItemRecord.objects.all()
#     serializer_class = FoodItemRecordSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         try:
#             daily_record = DailyRecord.objects.get(date=timezone.now().date(), user=self.request.user)
#         except DailyRecord.DoesNotExist:
#             daily_record = DailyRecord.objects.create(date=timezone.now().date(), user=self.request.user)
#         serializer.save(daily_record=daily_record,user=self.request.user)

class FoodItemRecordCreate(generics.ListCreateAPIView):
    queryset = FoodItemRecord.objects.all()
    serializer_class = FoodItemRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        food_item = FoodItem.objects.get(id=self.request.data.get('food_item'))
        try:
            daily_record = DailyRecord.objects.get(date=timezone.now().date(), user=self.request.user)
        except DailyRecord.DoesNotExist:
            daily_record = DailyRecord.objects.create(date=timezone.now().date(), user=self.request.user)
        serializer.save(daily_record=daily_record, food_item=food_item.id)
    
    
class ActivityRecordCreate(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(created=self.request.user)
        if self.request.user.is_staff:
            serializer.save(is_global = True,approved_by_admin = True)
        else:
            serializer.save(is_global = False,approved_by_admin = False)
    
    


class FoodItemRecordView(APIView):
    permission_classes = [permissions.IsAuthenticated]    
    
    def post(self, request):
        food_item = request.data.get("food_item")
        amount = request.data.get("amount")

        food_item_instance=FoodItem.objects.filter(name__icontains=food_item).first()
        try:
            daily_record = DailyRecord.objects.get(date=timezone.now().date(), user=self.request.user)
        except DailyRecord.DoesNotExist:
            daily_record = DailyRecord.objects.create(date=timezone.now().date(), user=self.request.user)
        FoodItemRecord.objects.create(food_item=food_item_instance,daily_record=daily_record,amount=amount)

        return Response({"success": "Food Item Created"})
 
 
class ActivityRecordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        activity = request.data.get("activity")
        duration = request.data.get("duration")

        activity_instance=Activity.objects.filter(name__icontains=activity).first()
        try:
            daily_record = DailyRecord.objects.get(date=timezone.now().date(), user=self.request.user)
        except DailyRecord.DoesNotExist:
            daily_record = DailyRecord.objects.create(date=timezone.now().date(), user=self.request.user)
        ActivityRecord.objects.create(activity=activity_instance,daily_record=daily_record,duration=duration)

        return Response({"success": "Activity Record Created"})


class RecordList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        daily_activity_durations = ActivityRecord.objects.values('activity__name','daily_record__date').annotate(duration_sum=Sum('duration'))
        daily_food_item_amount = FoodItemRecord.objects.values('food_item__name','daily_record__date').annotate(duration_sum=Sum('amount'))
        monthly_activity_duration = ActivityRecord.objects.annotate(month=ExtractMonth('daily_record__date'), year=ExtractYear('daily_record__date')).values('month', 'year','activity__name').annotate(sum_duration=Sum('duration'))
        monthly_food_item_amount = FoodItemRecord.objects.annotate(month=ExtractMonth('daily_record__date'), year=ExtractYear('daily_record__date')).values('month', 'year','food_item__name').annotate(sum_amount=Sum('amount'))


        return Response({"daily_activity":daily_activity_durations,"daily_food_item_amount":daily_food_item_amount,"monthly_activity":monthly_activity_duration,"monthly_food_item_amount":monthly_food_item_amount})



