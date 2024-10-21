from django.urls import path
from . import views


urlpatterns = [
    path('generate/', views.generate_hash_view, name='generate_hash'),
    path('verify/', views.verify_hash_view, name='verify_hash'),
    path('crack/', views.crack_hash_view, name='crack_hash'),
]