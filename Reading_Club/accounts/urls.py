from django.urls import path, include
from Reading_Club.accounts.views import UserLoginView, UserRegisterView, UserLogoutView, ProfileDetailsView, ProfileEditeView

app_name = "accounts"

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileDetailsView.as_view(), name="details"),
    path("profile/edit/", ProfileEditeView.as_view(), name="edit"),
]