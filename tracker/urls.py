from .views import index
from django.urls import path
from . import views

urlpatterns = [
    path("", index, name="index"),
    path("delete/<int:transaction_id>/", views.delete_transaction, name="delete_transaction"),
]
