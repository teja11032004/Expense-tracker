from django.contrib import admin
from tracker.models import CurrentBalance,TrackingHistory   


admin.site.site_header = "Expense Tracker"
admin.site.site_title = "Expense Tracker Admin Portal"
admin.site.site_url="Expense Tracker url"

 
admin.site.register(CurrentBalance)

@admin.action(description='Mark selected Stories as Credit')
def make_credit(modeladmin, request, queryset):
    for q in queryset:
        obj=TrackingHistory.objects.get(id=q.id)
        if obj.amount <0:
            obj.amount = abs(obj.amount)
            obj.save()

    queryset.update(expense_type='Credit')


admin.site.disable_action('delete_selected')

@admin.action(description='Mark selected Stories as Debit')
def make_debit(modeladmin, request, queryset):
    for q in queryset:
        obj=TrackingHistory.objects.get(id=q.id)
        if obj.amount >0:
            obj.amount = obj.amount * -1
            obj.save()
            

    queryset.update(expense_type='Debit')


class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'expense_type', 'current_balance' ,'description', 'created_at', 'updated_at', 'display_type']
    search_fields = ['description', 'amount']
    ordering = ['-expense_type']
    list_filter = ['expense_type', 'created_at']
    
    actions = [make_credit, make_debit]


    def display_type(self, obj):
        return "positive" if obj.expense_type == "Credit" else "negative"
    



admin.site.register(TrackingHistory, TrackingHistoryAdmin)

# Register your models here.

"""
from django.contrib.auth.models import User

In [2]: user=User.objects.first()

In [3]: user.username
Out[3]: 'teja'
user.password   --- display the hashed password
In [4]: user.set_password('newpassword123')
In [5]: user.save()

"""