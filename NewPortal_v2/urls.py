from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView, LogoutView, SignupView
from django.conf.urls import handler403
from django.views.generic import TemplateView

#handler403 = 'news.views.custom_permission_denied'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),

    path('accounts/', include('allauth.urls')),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),

    path(
        '1/',
        TemplateView.as_view(
            template_name='flatpages/home.html'),
        name='home'),

]
