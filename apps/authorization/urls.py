from django.urls import path
from authorization import views

app_name = 'auth'

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-up-confirm/<uuid:key>/', views.SignUpConfirmView.as_view(), name='sign-up-confirm'),
    path('sign-in/', views.SignInView.as_view()),

    # path('logout/', )

]
