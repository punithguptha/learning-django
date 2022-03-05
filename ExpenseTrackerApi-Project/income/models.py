from django.db import models
from authentication.models import User

# Create your models here.

class Income(models.Model):

    SOURCE_OPTIONS=[
        ("SALARY","SALARY_HUMAN_READABLE_FIELD"),
        ("BUSINESS","BUSINESS_HUMAN_READABLE_FIELD"),
        ("SIDE_HUSTLES","SIDE_HUSTLES_HUMAN_READABLE_FIELD"),
        ("OTHERS","OTHERS_HUMAN_READABLE_FIELD")
    ]

    source=models.CharField(choices=SOURCE_OPTIONS,max_length=255)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(null=False,blank=False)

    # Meta in models generally is used to store additional information corresponding to a model
    class Meta:
        ordering:['-date']

    def __str__(self):
        return str(self.owner)+'s income'
