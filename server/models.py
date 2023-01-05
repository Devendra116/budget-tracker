from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class UserModel(models.Model):
#     name = models.CharField(max_length=200, blank=True)
#     # username = models.CharField(max_length=200, primary_key=True)
#     email = models.EmailField(unique=True)
#     password=models.CharField(max_length=30)
#     # income = models.FloatField()
#     # expense = models.FloatField()
#     # budget = models.FloatField()
#     # owe_balance = models.FloatField()
#     # credit_balance = models.FloatField()
#     profile_created = models.DateTimeField(auto_now=True)
#     profile_updated = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    income = models.FloatField(default=0)
    expense = models.FloatField(default=0)
    budget = models.FloatField(default=0)
    owe_balance = models.FloatField(default=0)
    credit_balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.user)

class TransactionModel(models.Model):
    BUDGET_CATEGORY = (
        ('Fuel/Gas', 'Fuel/Gas'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
    )
    TRANSACTION_TYPE = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )
    transaction_note = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=BUDGET_CATEGORY)
    amount = models.FloatField()
    transaction_type = models.CharField(
        max_length=200, choices=TRANSACTION_TYPE)
    payer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='transaction_payer',null=True)
    transc_creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='transc_creator', null=True)
    is_bill_splitted = models.BooleanField(default=False)
    totalfriend=models.IntegerField(default=0)
    transaction_created = models.DateTimeField(auto_now=True)
    transaction_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_note

    def save(self, *args, **kwargs):
        if self.is_bill_splitted=='on':
            self.is_bill_splitted=True
        else:
            self.is_bill_splitted=False
        super(TransactionModel, self).save(*args, **kwargs)


class SplitBillModel(models.Model):
    transac_bill_id = models.ForeignKey(
        TransactionModel, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bill_amount=models.FloatField(default=0)
    bill_paid = models.BooleanField(default=False)
    bill_paid_on = models.DateTimeField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)