from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView,CreateAPIView
from store.serializers import ProductSerializer
from store.models import Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

class ProductsPagination(LimitOffsetPagination):
    default_limit=10
    max_limit=100

# https://www.django-rest-framework.org/api-guide/generic-views/ Refer to this to understand about generic views that drf provides and the params that are available for each
class ProductList(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=(DjangoFilterBackend,SearchFilter) #This can also be declared at the global level or at view level like this
    filter_fields=('id',) #The options to specify by which the filtering should occur..Hit the endpoint to understand more(Like this http://127.0.0.1:8000/api/v1/products?id=1)
    # One can also set the type of the search to be made..By default it is Partial Match..The other options available are Exact Match and Regular Expression
    # Refer to this https://www.django-rest-framework.org/api-guide/filtering/#searchfilter for more details on the same
    search_fields=('name','description')

    # Below is to set the pagination option.To try use this http://127.0.0.1:8000/api/v1/products?offset=1&limit=2
    # Offset describes which page to go to and limit describes the max entries in a page
    pagination_class=ProductsPagination

    #To filter products based on if they are on sale or not..For this we have to override the get_queryset method
    # Look into queryset.filter in django to understand more
    def get_queryset(self):
        on_sale=self.request.query_params.get('on_sale',None)
        if on_sale is None:
            return super().get_queryset()
        queryset=Product.objects.all()
        # For this to work properly set the sale_end_date for some products greater than today from the django admin db site
        if on_sale.lower()=="true":
            from django.utils import timezone
            now=timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__gte=now,
            )
        return queryset

class ProductCreationAPIView(CreateAPIView):
    serializer_class=ProductSerializer

    def create(self,request,*args,**kwargs):
        try:
            price=request.data.get('price')
            if price is not None and float(price)<=0.0:
                raise ValidationError({'price':'Must be above $0.00'})
        except ValueError:
            raise ValidationError({'price':'Must be a valid number'})
        return super().create(request,*args,**kwargs)
