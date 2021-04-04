from django.urls import path
from notification import views

urlpatterns = [
    path('telegram/', views.TelegramConfirmationCreateView.as_view())
]