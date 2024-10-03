
from django.urls import path
from auth_api.views import *

app_name = "auth_api"

urlpatterns = [
  path("register/", UserRegistrationView.as_view(), name="register"),
  path("login/", UserLoginView.as_view(), name="login"),
  path("profile/", UserProfileView.as_view(), name="profile"),
]