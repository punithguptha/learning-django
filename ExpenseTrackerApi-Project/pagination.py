from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class ExpensePaginationGlobal(PageNumberPagination):
    page_size=10
