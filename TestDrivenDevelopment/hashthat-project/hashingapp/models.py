from django.db import models

# Create your models here.

class HashModel(models.Model):
    text=models.TextField()
    # Max length 64 since sha256 encoding always returns in 64 length output string
    hashed_text=models.CharField(max_length=64)
