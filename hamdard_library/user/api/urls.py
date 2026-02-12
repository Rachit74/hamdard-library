from django.urls import path
from .views import login_user, protected_view, register_user
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("auth/login/", csrf_exempt(login_user)),
    path("auth/register/", csrf_exempt(register_user)),
    path("auth/special/", protected_view),

    path('auth/token/refresh/', TokenRefreshView.as_view()),  # refreshes access token
]