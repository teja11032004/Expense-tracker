from django.shortcuts import render,redirect
from .models import CurrentBalance,TrackingHistory
from django.contrib import messages


# Create your views here.
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