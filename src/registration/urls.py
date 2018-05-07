from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from allauth.account.views import LoginView, PasswordResetView, SignupView

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name="logout"),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='store/registration/password_reset_email.html'), name="password_reset"),
    # path('password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name="password_reset_confirm"),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name="password_reset_complete"),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    # path('signup/', views.signup, name='signup'),
    # path('account_login/', LoginView.as_view(template_name='registration/login.html'), name="account_login"),
    # path('account_reset_password/', PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='store/registration/password_reset_email.html'), name="account_reset_password"),
    # path('account_signup/', SignupView, name='account_signup'),
    
] 