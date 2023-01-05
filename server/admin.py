from django.contrib import admin
from .models import TransactionModel,SplitBillModel,Profile
# Register your models here.
admin.site.register(TransactionModel)
admin.site.register(SplitBillModel)
admin.site.register(Profile)