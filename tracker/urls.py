from .views import index
from django.urls import path
from . import views

urlpatterns = [
    path("", index, name="index"),
    path("login/", views.login_view, name="login_page"),
    path("register/", views.register_view, name="register_page"),
    path("logout/", views.logout_view, name="logout_page"),
    path("delete/<int:transaction_id>/", views.delete_transaction, name="delete_transaction"),
]
