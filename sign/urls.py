from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me
from .views import signup, activate

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='sign/login.html'),
        name='login'),

    path(
        'logout/',
        LogoutView.as_view(
            template_name='sign/logout.html'),
        name='logout'),

    path(
        'signup/',
        BaseRegisterView.as_view(
            template_name='sign/signup.html'),
        name='signup'),

    path('upgrade/', upgrade_me, name='upgrade'),

    path('signup/', signup, name='signup'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
