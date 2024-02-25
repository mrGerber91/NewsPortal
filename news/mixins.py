from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class AuthCheckMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')  # URL страницы входа
    redirect_field_name = 'next'

    def handle_no_permission(self):
        # Если пользователь аутентифицирован, перенаправляем его на главную
        # страницу
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('news_list'))
        # Если пользователь не аутентифицирован, перенаправляем его на страницу
        # входа или регистрации
        else:
            return HttpResponseRedirect(self.login_url)
