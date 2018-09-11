from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)
from . import views
app_name = 'authentication'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='update_user'),
    path('users/', RegistrationAPIView.as_view(), name='user_signup'),
    path('users/login/', LoginAPIView.as_view(), name='user_login'),
    path('users/verify/<uidb64>/<token>/',
         views.VerifyAPIView.as_view(), name='verify'),
    path('users/forgot_password/', views.UserForgetPasswordView.as_view(),
         name='forgot_pass'),
    path('users/reset_password/<token>/',
         views.ResetPasswordLinkView.as_view(),
         name='reset_password')

]
