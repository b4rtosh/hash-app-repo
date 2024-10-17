from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.des_encrypt_view, name='des_encrypt'),
    path('decrypt/', views.des_decrypt_view, name='des_decrypt'),
    ]