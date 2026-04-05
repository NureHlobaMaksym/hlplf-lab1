from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import EmailAuthenticationForm, SignUpForm
from accounts.models import User


class EmailLoginView(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'registration/login.html'


class EmailLogoutView(LogoutView):
    next_page = reverse_lazy('article_list')


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def redirect_logout(request):
    return redirect('article_list')
