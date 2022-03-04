# exec(open("scripts/testscript2.py").read()) ->To execute this file in django shell
from expenses.models import Expense
from rest_framework.renderers import JSONRenderer
from expenses.serializers import ExpenseSerializer

# serializer=RegisterSerializer()
# entry=User.objects.get(email="testuser@gmail.com")
serializer=ExpenseSerializer()
entry=Expense.objects.first()
data=serializer.to_representation(entry)
renderer=JSONRenderer()
print(renderer.render(data))
