from django.contrib import admin
from .models import Transactions, UserProfile

# Register your models here.
admin.site.register(Transactions)
admin.site.register(UserProfile)
