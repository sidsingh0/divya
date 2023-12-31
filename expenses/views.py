from django.shortcuts import render, redirect
from .models import Transactions, UserProfile
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == 'POST':
        ttype = request.POST.get('incomeExpense')
        label = request.POST.get('label')
        amount_str = request.POST.get('amount')

        if not amount_str or not amount_str.strip():  # Check for empty or whitespace-only input
            contextdata = {'msg': '<script>alert("Amount must not be empty.")</script>', 'current_user': request.user}
            return render(request, "index.html", context=contextdata)
        if not label or not label.strip():  # Check for empty or whitespace-only input
            contextdata = {'msg': '<script>alert("Text must not be empty.")</script>', 'current_user': request.user}
            return render(request, "index.html", context=contextdata)

        try:
            amount = int(amount_str)
        except (ValueError, TypeError):
            contextdata = {'msg': '<script>alert("Amount must be a valid number.")</script>', 'current_user': request.user}
            return render(request, "index.html", context=contextdata)

        Transactions.objects.create(ttype=ttype, amount=amount, label=label, user=request.user)

        contextdata = {'msg': '<script>alert("Successfully added your transaction.")</script>', 'current_user': request.user}
        return render(request, "index.html", context=contextdata)
    else:
        return render(request, "index.html", {'current_user': request.user})

@login_required
def balance(request):    
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    if(current_user.username != "admin"):
        profile = UserProfile.objects.get(user=user)
    else:
        return redirect("home")
    # Calculate the total amount for the current user where ttype is False
    
    total_income = Transactions.objects.filter(user=current_user, ttype=True).aggregate(Sum('amount'))['amount__sum']
    if total_income is None:
        total_income = 0  # Set to 0 if there are no matching transactions
    
    total_expense = Transactions.objects.filter(user=current_user, ttype=False).aggregate(Sum('amount'))['amount__sum']
    if total_expense is None:
        total_expense = 0  # Set to 0 if there are no matching transactions
    
    context = {'total_income': total_income,'total_expense':total_expense,'total_balance':total_income-total_expense, 'current_user': request.user,'user':user,'profile':profile}
    return render(request, "balance.html",context)

@login_required
def history(request):
    current_user = request.user
    sorted_transactions = Transactions.objects.filter(user=current_user).order_by('-timestamp')
    context = {'sorted_transactions': sorted_transactions, 'current_user': request.user}
    return render(request, "history.html",context)

@login_required
def statistics(request):
    current_user = request.user
    # Calculate the total amount for the current user where ttype is False
    
    total_income = Transactions.objects.filter(user=current_user, ttype=True).aggregate(Sum('amount'))['amount__sum']
    if total_income is None:
        total_income = 0  # Set to 0 if there are no matching transactions
    
    total_expense = Transactions.objects.filter(user=current_user, ttype=False).aggregate(Sum('amount'))['amount__sum']
    if total_expense is None:
        total_expense = 0  # Set to 0 if there are no matching transactions
    
    context = {'total_income': total_income,'total_expense':total_expense, 'current_user': request.user}
    return render(request, "statistics.html",context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Create a UserProfile instance for the user
            profile_picture = form.cleaned_data.get('image')
            phone = form.cleaned_data.get('phone')
            UserProfile.objects.create(user=user, profile_picture=profile_picture,phone=phone)

            # Log in the user
            login(request, user)
            
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form, 'current_user': request.user})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other desired page upon successful login
        else:
            contextdata = {'msg': '<script>alert("Invalid login credentials. Please try again.")</script>', 'current_user': request.user}
            return render(request, 'login.html', context=contextdata)
    else:
        return render(request, 'login.html',{'current_user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')

def delete(request,id):
    txn = Transactions.objects.get(id=id)
    txn.delete()
    return redirect("history")

