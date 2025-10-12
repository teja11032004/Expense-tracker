from django.db import models


class CurrentBalance(models.Model):
    amount = models.FloatField(default=0.0)

# Create your models here.
class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_type = models.CharField(max_length=100,choices=(('Credit','Credit'),('Debit','Debit')))
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount} on {self.date}"