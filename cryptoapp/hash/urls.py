from django.urls import path
from . import views


urlpatterns = [
    path('generate/', views.generate_hash_view, name='generate_hash'),
    ]