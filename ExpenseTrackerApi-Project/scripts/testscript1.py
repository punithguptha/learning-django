# exec(open("scripts/testscript1.py").read()) ->To execute this file in django shell
from authentication.models import User
from authentication.serializers import RegisterSerializer,LoginSerializer
from rest_framework.renderers import JSONRenderer

# serializer=RegisterSerializer()
# entry=User.objects.get(email="testuser@gmail.com")
serializer=LoginSerializer()
entry=User.objects.first()
data=serializer.to_representation(entry)
renderer=JSONRenderer()
print(renderer.render(data))
