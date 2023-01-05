from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import TransactionModel,Profile,SplitBillModel


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class TransactionForm(ModelForm):
    class Meta: 
        model = TransactionModel
        fields='__all__'

class ProfileForm(ModelForm):
    class Meta: 
        model = Profile
        fields='__all__'

class BillForm(ModelForm):
    class Meta: 
        model = SplitBillModel()
        fields='__all__'


