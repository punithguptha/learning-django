from rest_framework import serializers
from store.models import Product,ShoppingCartItem

class ShoppingCartItemSerializer(serializers.ModelSerializer):
    quantity=serializers.IntegerField(min_value=1,max_value=100)

    class Meta:
        model=ShoppingCartItem
        fields=('product','quantity')

class ProductSerializer(serializers.ModelSerializer):

    is_on_sale=serializers.BooleanField(read_only=True)
    current_price=serializers.FloatField(read_only=True)
    description=serializers.CharField(min_length=2,max_length=200)
    carts_containing_items=serializers.SerializerMethodField()
    # price= serializers.FloatField(min_value=1.00, max_value=100000)
    price=serializers.DecimalField(
        min_value=1.00,max_value=100000,
        max_digits=None,decimal_places=2,
    )
    sale_start=serializers.DateTimeField(
        input_formats=['%I:%M %p %d %B %Y'], format=None,allow_null=True,
        help_text='Accepted format is "12:01 PM 19 February 2022"',
        style={'input_type':'text','placeholder':'12:01 AM 28 July 2019'},
    )

    sale_end=serializers.DateTimeField(
        input_formats=['%I:%M %p %d %B %Y'], format=None,allow_null=True,
        help_text='Accepted format is "12:01 PM 19 February 2022"',
        style={'input_type':'text','placeholder':'12:01 AM 28 July 2019'},
    )

    photo = serializers.ImageField(default=None)
    # Write only indicates that it is just used in the api but doesnot get saved to the model
    warranty= serializers.FileField(write_only=True,default=None)

    class Meta:
        model= Product
        fields=('id','name','description','price','sale_start','sale_end','is_on_sale','current_price','carts_containing_items',
        'photo','warranty',
        )

    def get_carts_containing_items(self,instance):
        items=ShoppingCartItem.objects.filter(product=instance)
        return ShoppingCartItemSerializer(items,many=True).data

    # Validated data is that data which is already passed through the serializer and model validation process. It is used to create or update a model
    def update(self,instance,validated_data):
        if validated_data.get('warranty',None):
            instance.description += '\n\nWarranty Information:\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
            return instance
class ProductStatSerializer(serializers.Serializer):
    # The dictfield can take values of any type but the key must be a string
    stats= serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        )
    )
