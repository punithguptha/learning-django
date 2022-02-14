# These are the scripts for testing.
# To execute a script in django shell first open the shell and then use exec(open("DjangoShellScripts/script1.py").read())
from store.serializers import *
from store.models import *
from rest_framework.renderers import JSONRenderer

# To Test the Serializer and its working
product =Product.objects.all()[0]
serializer=ProductSerializer()
data=serializer.to_representation(product)
renderer=JSONRenderer()
print(renderer.render(data))
