from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm, TransactionForm, ProfileForm, BillForm
from .models import SplitBillModel, TransactionModel, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction
from django.template.defaulttags import register

@transaction.atomic
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        profile=ProfileForm()
        user=User.objects.get(username=user_obj)
        profile=Profile.objects.create(user=user)
        return redirect('/user')
    context = {'form': form}
    return render(request, 'register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/user')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/user')
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    logout(request)
    return redirect('/user')


def getUserDetail(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    userId = request.user.id
    user = User.objects.get(pk=userId)
    transactions = TransactionModel.objects.filter(transc_creator=userId)
    bills = SplitBillModel.objects.filter(payer=userId)
    context = {'user': user, 'transactions': transactions, 'bills': bills}
    return render(request, 'home.html', context)

@transaction.atomic
def update_profile(request):
    user_obj = User.objects.get(id=request.user.id)
    print(user_obj)

    userform = UserForm(instance=user_obj)
    profile_obj = Profile.objects.get(user=user_obj)
    print(profile_obj)
    profileform = ProfileForm(instance=profile_obj)
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=user_obj)
        profileform = ProfileForm(request.POST, instance=profile_obj)
        if userform.is_valid() and profileform.is_valid():
            user_ = userform.save()
            profile = profileform.save(commit=False)
            profile.user = user_
            profile.save()
            return redirect('/user')
    context = {'user': userform, 'profile': profileform,'username':request.user}
    return render(request, 'profile.html', context)


def update_transaction(request, pk):
    transaction = TransactionModel.objects.get(id=pk)
    transactionform = TransactionForm(instance=transaction)
    bill = SplitBillModel.objects.filter(transac_bill_id=transaction.id)
    bill_payers = [x for x in bill]
    for i in bill_payers:
        print(i)
    print(bill_payers)
    if request.method == 'POST':
        transactionform = TransactionForm(request.POST, instance=transaction)
        if transactionform.is_valid():
            transactionform = transactionform.save()
            if request.POST.get('totalfriend'):
                for payer in bill_payers:
                    print(transactionform)
                    bill = SplitBillModel.objects.get(id=payer.id)
                    current_bill_amount = bill.bill_amount
                    bill.bill_amount = transactionform.amount /int(request.POST.get('totalfriend'))
                    current_profile = Profile.objects.get(user=payer.payer)
                    if transaction.transaction_type=='Income':
                        print("Income")
                        current_profile.income = (current_profile.income+bill.bill_amount-current_bill_amount)
                    else:
                        current_profile.expense = current_profile.expense+bill.bill_amount-current_bill_amount
                        print("Expense")

                    current_profile.save()
                    bill.save()
            else:
                bill = SplitBillModel.objects.get(id=transaction.id)
                current_bill_amount = bill.bill_amount
                bill.bill_amount = transactionform.amount /int(request.POST.get('totalfriend'))
                current_profile = Profile.objects.get(user=transaction.payer)
                if transaction.transaction_type=='Income':
                    print("Income")
                    current_profile.income = (current_profile.income+bill.bill_amount-current_bill_amount)
                else:
                    current_profile.expense = current_profile.expense+bill.bill_amount-current_bill_amount
                    print("Expense")

                current_profile.save()
                bill.save()

            return redirect('/user')
    context = {'form': transactionform, 'bill_payers': bill_payers}
    return render(request, 'update_transaction.html', context)


def delete_transaction(request, pk):
    transaction = TransactionModel.objects.get(id=pk)
    # only creator can delete
    if not transaction.transc_creator == request.user:
        return redirect('/user')
    if transaction.is_bill_splitted:
        bills = SplitBillModel.objects.filter(transac_bill_id=transaction.id)
        bills.delete()
    transaction.delete()
    return redirect('/user')


@transaction.atomic
def createTransaction(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            print(request.POST)
            if request.POST.get('totalfriend'):
                for i in range(1, int(request.POST.get('totalfriend'))+1):
                    bill = SplitBillModel()
                    bill.transac_bill_id = TransactionModel.objects.get(pk=transaction.id)
                    bill.bill_amount = transaction.amount /int(request.POST.get('totalfriend'))
                    bill.payer = User.objects.get(username=request.POST.get('friend'+str(i)))
                    if bill.payer == request.user:
                        bill.bill_paid = True
                    else:
                        bill.bill_paid = False
                    current_user = Profile.objects.get(user=bill.payer)
                    if request.POST.get('transaction_type')=='Income':
                        print("Income")
                        current_user.income = current_user.income+bill.bill_amount
                    else:
                        print("Expense")
                        current_user.expense = current_user.expense+bill.bill_amount
                    
                    current_user.save()
                    bill.save()
            else:
                bill = SplitBillModel()
                bill.transac_bill_id = TransactionModel.objects.get(pk=transaction.id)
                bill.bill_amount = transaction.amount
                bill.payer = request.user
                if bill.payer == request.user:
                    bill.bill_paid = True
                else:
                    bill.bill_paid = False
                current_user = Profile.objects.get(user=bill.payer)
                if request.POST.get('transaction_type')=='Income':
                    print("Income")
                    current_user.income = current_user.income+bill.bill_amount
                else:
                    print("Expense")
                    current_user.expense = current_user.expense+bill.bill_amount
                current_user.save()
                bill.save()
            return redirect('/user')
    context = {'form': form,'username':request.user}
    return render(request, 'transaction.html', context)


def show_bill(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    bill = SplitBillModel.objects.filter(payer=request.user.id)
    context = {'data': bill}
    return render(request, 'demo.html', context)

def update_bill(request, id):
    bill = SplitBillModel.objects.get(pk=id)
    form = BillForm(instance=bill)
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('/user')
    context = {'form': form}
    return render(request, 'bill.html', context)


def edit_bill(request, transaction_id):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    bill = SplitBillModel.objects.get(transac_bill_id=transaction_id)
    context = {'data': bill}
    return render(request, 'demo.html', context)

 
