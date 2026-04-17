from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from Reading_Club.accounts.forms import RegisterUserForm, LoginUserForm, EditProfileForm
from Reading_Club.accounts.models import BaseUser


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginUserForm
    redirect_authenticated_user = True


class UserRegisterView(CreateView):
    model = BaseUser
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = BaseUser
    template_name = 'accounts/user_profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_wishlist_ids'] = set(
            self.request.user.wishlist.values_list('id', flat=True)
        )
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = BaseUser
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:details')

    def get_object(self, queryset=None):
        return self.request.user