from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import FoodItem, FoodItemLabel, Activity, DailyRecord, FoodItemRecord, ActivityRecord
from .serializers import *
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

# from django.http import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import login
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear



class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(created=self.request.user)
        if self.request.user.is_staff:
            serializer.save(is_global = True,approved_by_admin = True)
        else:
            serializer.save(is_global = False,approved_by_admin = False)

class FoodItemLabelViewSet(viewsets.ModelViewSet):
    queryset = FoodItemLabel.objects.all()
    serializer_class = FoodItemLabelSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(created=self.request.user)
        if self.request.user.is_staff:
            serializer.save(is_global = True,approved_by_admin = True)
        else:
            serializer.save(is_global = False,approved_by_admin = False)

class DailyRecordViewSet(viewsets.ModelViewSet):
    queryset = DailyRecord.objects.all()
    serializer_class = DailyRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class FoodItemRecordViewSet(viewsets.ModelViewSet):
    queryset = FoodItemRecord.objects.all()
    serializer_class = FoodItemRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            daily_record = DailyRecord.objects.get(date=timezone.now().date(), user=self.request.user)
        except DailyRecord.DoesNotExist:
            daily_record = DailyRecord.objects.create(date=timezone.now().date(), user=self.request.user)
        serializer.save(daily_record=daily_record,user=self.request.user)


class ActivityRecordViewSet(viewsets.ModelViewSet):
    queryset = ActivityRecord.objects.all()
    serializer_class = ActivityRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            daily_record = DailyRecord.objects.get(date=timezone.now().date(), user=self.request.user)
        except DailyRecord.DoesNotExist:
            daily_record = DailyRecord.objects.create(date=timezone.now().date(), user=self.request.user)
        serializer.save(daily_record=daily_record,user=self.request.user)

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



