from .views import ExpenseSummaryStatsAPIView
from django.urls import path


urlpatterns=[
    path('expense_category_data/',ExpenseSummaryStatsAPIView.as_view(),name="expense_category_summary"),
]
