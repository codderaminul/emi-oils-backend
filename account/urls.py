from django.urls import include, path
from account.views import LoginView,SignupView,VerifyOTPView,LogoutView,ForgotPasswordView,Profile,social_signup,social_login,new_set_password

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('social/login/', social_login, name='social_login'),
    path('social/signup/', social_signup, name='social_signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('my-profile/', Profile.as_view(), name='profile'),
    path("VerifyOTP/", VerifyOTPView.as_view(), name="VerifyOTP"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('new-set-password/<int:user_id>',new_set_password,name='new_set_password'),

    # path("my-profile/", MyProfileView.as_view(), name="my_profile"),
    # path("check-email/", check_email, name="check_email"),
    # path("change-email/", change_email, name="change_email"),
    # # user preferred path 
    # path("social/login/", social_login, name="social_login"),
]