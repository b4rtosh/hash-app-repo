from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.des_encrypt_view, name='des_encrypt'),
    path('crack/', views.des_crack_view, name='des_crack'),
    ]