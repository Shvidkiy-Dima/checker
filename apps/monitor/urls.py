from django.urls import path
from monitor import views

app_name = 'monitor'

urlpatterns = [
    path('', views.MonitorView.as_async_view(), name='monitor'),
    path('<uuid:pk>/', views.MonitorDetailView.as_view(), name='monitor_detail')
]

