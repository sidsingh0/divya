from django.db import models
from django.contrib.auth.models import User

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=500)
    amount = models.IntegerField()
    ttype = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
