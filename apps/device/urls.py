from django.urls import path
from device import views


urlpatterns = [
    path('', views.FCMView.as_view(), name='fcm_device'),
]