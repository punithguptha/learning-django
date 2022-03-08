from django.shortcuts import render
from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from income.models import Income
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

class ExpenseSummaryStatsAPIView(APIView):

    def get(self,request):
        todays_date=datetime.date.today()
        year_ago_date=todays_date-datetime.timedelta(days=365)
        try:
            expenses=Expense.objects.filter(owner=request.user,date__gte=year_ago_date,date__lte=todays_date)
        except Exception as e:
            raise AuthenticationFailed("Invalid credentials or user not logged in..Please check and try again!!")

        final_data={}


        for expense in expenses:
            if expense.category not in final_data:
                final_data[expense.category]={}
                final_data[expense.category]["amount"]=0
            final_data[expense.category]["amount"]+=expense.amount

        for keys in final_data:
            final_data[keys]["amount"]=str(final_data[keys]["amount"])
        return Response({'expense_category_data':final_data},status=status.HTTP_200_OK)


class IncomeSummaryStatsAPIView(APIView):

    def get(self,request):
        todays_date=datetime.date.today()
        year_ago_date=todays_date-datetime.timedelta(days=365)
        try:
            income_all=Income.objects.filter(owner=request.user,date__gte=year_ago_date,date__lte=todays_date)
        except Exception as e:
            raise AuthenticationFailed("Invalid credentials or user not logged in..Please check and try again!!")

        final_data={}


        for income in income_all:
            if income.source not in final_data:
                final_data[income.source]={}
                final_data[income.source]["amount"]=0
            final_data[income.source]["amount"]+=income.amount

        for keys in final_data:
            final_data[keys]["amount"]=str(final_data[keys]["amount"])
        return Response({'income_source_data':final_data},status=status.HTTP_200_OK)
