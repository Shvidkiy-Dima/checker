from django.urls import path
from monitor import views

urlpatterns = [
    path('', views.MonitorView.as_async_view()),
    path('<uuid:pk>/', views.MonitorDetailView.as_view())
]