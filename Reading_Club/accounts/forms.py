from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from Reading_Club.accounts.models import BaseUser


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = BaseUser
        fields = ['username', 'nickname', 'email', 'profile_image', 'password1', 'password2']
        labels = {'username': 'Username', 'nickname': 'Nickname', 'email': 'Email', 'profile_image': 'Profile image'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter nickname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'username': {'unique': 'This username is already taken.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].required = True
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repeat password'})


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['username', 'nickname', 'email', 'bio', 'profile_image']
        labels = {
            'username': 'Username',
            'nickname': 'Nickname',
            'email': 'Email',
            'bio': 'About me',
            'profile_image': 'Profile image',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell others a bit about yourself...'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['nickname'].required = True