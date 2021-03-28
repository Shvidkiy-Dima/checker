from django.urls import path
from monitor import views

urlpatterns = [
    path('', views.MonitorView.as_view()),
    # path('<uuid:id>/', views.M)
]