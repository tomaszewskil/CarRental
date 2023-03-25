from django.urls import path
from .views import loginPage, registerPage, logoutUser, activate, profilePage, rentHistoryPage, passwordChange, \
    passwordReset, passwordResetConfirm

urlpatterns = [
    path("login/", loginPage, name='login'),
    path("register/", registerPage, name="register"),
    path("logout/", logoutUser, name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('profile/<username>/', profilePage, name='profile'),
    path('profile/<username>/rentHistory/', rentHistoryPage, name='rent_history'),
    path("password_change/", passwordChange, name='password_change'),
    path("password_reset/", passwordReset, name='password_reset'),
    path("reset/<uidb64>/<token>", passwordResetConfirm, name='password_reset_confirm'),
]
