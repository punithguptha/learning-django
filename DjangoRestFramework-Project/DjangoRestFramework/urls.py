"""DjangoRestFramework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import store.views
from store.api_views import ProductList
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r'modelviewset',store.api_views.ProductCrudAPIView)


urlpatterns = [
    path('api/v1/products',store.api_views.ProductList.as_view()), #Generally views are function based but if they are class based we need to define this way
    path('api/v1/products/create',store.api_views.ProductCreationAPIView.as_view()),
    path('api/v1/products/<int:id>/delete',store.api_views.ProductDeletionAPIView.as_view()),
    path('api/v1/products/<int:id>/rud',store.api_views.ProductRetrieveUpdateDestroyAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('products/<int:id>/',store.views.show, name='show-product'),
    path('cart/',store.views.cart,name='shopping-cart'),
    path('',store.views.index, name='list-products'),
    # The below is for modelviewset based approach where the mapping will be of the type api/v1/modelviewset/pk. And for create part pk doesnt exist
    # The other thing is it handles all the crud opereations without needing to mention in the url. It takes the params from the request.method and does the thing accordingly.
    path('api/v1/',include(router.urls)),
]


# Below lines are for handling the static files
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
