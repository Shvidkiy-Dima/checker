from django.urls import path
from account import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view())
]