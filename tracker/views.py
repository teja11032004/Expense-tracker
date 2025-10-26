from django.shortcuts import render,redirect
from .models import CurrentBalance,TrackingHistory
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user=User.objects.filter(username=username)
        if not user.exists():
            messages.error(request, "Username does not exist")
            return redirect("/login/")

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("/login/")
    return render(request, "login.html")



def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("/register/")

        # ✅ Create the user properly
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)  # Hash the password
        user.save()

        messages.success(request, "User registered successfully. Please log in.")
        return redirect("/register/")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")
# Create your views here.
@login_required(login_url='login_page')
def index(request):
    if request.method == "POST":
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        current_balance = CurrentBalance.objects.get_or_create(id=1)[0]
        if float(amount) < 0:
            expense_type = "Debit"
        else:
            expense_type = "Credit" 

        if float(amount) ==0:
            messages.success(request, 'Amount cannot be zero')
            return redirect("/")
        tracking_history = TrackingHistory.objects.create(
            current_balance=current_balance,
            amount=amount,
            expense_type=expense_type,
            description=description)
        current_balance.amount += float(tracking_history.amount)
        current_balance.save()
        return redirect("/")
    

    current_balance = CurrentBalance.objects.get_or_create(id=1)[0]
    income = 0
    expense = 0
    for tracking_history in TrackingHistory.objects.all():
        if tracking_history.expense_type == "Credit":
            income += tracking_history.amount
        else:
            expense += tracking_history.amount

    context={'transactions':TrackingHistory.objects.all(),'balance':current_balance,'income':income,'expense':expense}
    return render(request, "index.html",context)

@login_required(login_url='login_page')
def delete_transaction(request, transaction_id):
    transaction = TrackingHistory.objects.get(id=transaction_id)
    current_balance = CurrentBalance.objects.get_or_create(id=1)[0]
    if transaction.expense_type == "Credit":
        current_balance.amount -= transaction.amount
    else:
        current_balance.amount -= transaction.amount
    current_balance.save()
    transaction.delete()
    return redirect("/")