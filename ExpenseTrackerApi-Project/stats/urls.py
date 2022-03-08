from .views import ExpenseSummaryStatsAPIView,IncomeSummaryStatsAPIView
from django.urls import path


urlpatterns=[
    path('expense_category_data/',ExpenseSummaryStatsAPIView.as_view(),name="expense_category_summary"),
    path('income_source_data/',IncomeSummaryStatsAPIView.as_view(),name="income_source_summary"),
]
