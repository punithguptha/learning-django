from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ExpenseSerializer
from .models import Expense
from rest_framework import permissions
from .permissions import IsOwner
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination


# Create your views here.

class ExpensePaginationTypeOne(LimitOffsetPagination):
    default_limit=10
    max_limit=100

class ExpensePaginationTypeTwo(PageNumberPagination):
    page_size=10


class ExpenseListAPIView(ListCreateAPIView):
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    # https://www.django-rest-framework.org/api-guide/pagination/ ->Refer to this doc for more details on pagination part
    # pagination_class=ExpensePaginationTypeOne
    # pagination_class=ExpensePaginationTypeTwo
    
    # Inbuilt method override
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    # Inbuilt method override
    def get_queryset(self):
        # import pdb; pdb.set_trace()
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsOwner,)
    lookup_field="id"

    # Inbuilt method override
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    # Inbuilt method override
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
