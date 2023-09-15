from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('verify/<str:email>/<uuid:UUID>/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('login/', views.custom_login_view, name='login'),  # views.UserLoginView.as_view(),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(views.UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
