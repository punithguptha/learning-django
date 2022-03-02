from authentication.models import User
from authentication.serializers import RegisterSerializer
from rest_framework.renderers import JSONRenderer

serializer=RegisterSerializer()
entry=User.objects.get(email="testuser@gmail.com")
data=serializer.to_representation(entry)
renderer=JSONRenderer()
print(renderer.render(data))
