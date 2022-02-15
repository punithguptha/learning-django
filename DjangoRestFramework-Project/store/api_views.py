from rest_framework.generics import ListAPIView
from store.serializers import ProductSerializer
from store.models import Product

# https://www.django-rest-framework.org/api-guide/generic-views/ Refer to this to understand about generic views that drf provides and the params that are available for each
class ProductList(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
