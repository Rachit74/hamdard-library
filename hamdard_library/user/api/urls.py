from django.urls import path
from .views import login_user, protected_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/login/", login_user),
    path("auth/special/", protected_view),

    path('auth/token/refresh/', TokenRefreshView.as_view()),  # refreshes access token
]