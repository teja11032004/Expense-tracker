from django.db import models
from django.contrib.auth.models import User


class CurrentBalance(models.Model):
    amount = models.FloatField(default=0.0)


    def __str__(self):
        return f"{self.amount}"

# Create your models here.
class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField(editable=False)
    expense_type = models.CharField(max_length=100,choices=(('Credit','Credit'),('Debit','Debit')))
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"The amount is {self.amount} for  {self.description} expense type is  {self.expense_type}"
    

class RequestLogs(models.Model):
    request_info = models.TextField()
    request_type = models.CharField(max_length=100)
    request_METHOD = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)