from django.urls import path
from account import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view()),
    path('alert/', views.AlertView.as_view()),
    path('alert/<int:pk>/', views.AlertDisableView.as_view()),
]