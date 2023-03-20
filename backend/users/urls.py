from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('auth/signup/', views.SignUp.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('profile/', views.ProfileListView.as_view(), name='profile'),
    path('buy/', views.ProfileListView.as_view(), name='buy'),
]
