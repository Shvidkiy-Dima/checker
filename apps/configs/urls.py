from django.urls import path
from configs import views

urlpatterns = [
    path('', views.UserConfigView.as_view()),
]