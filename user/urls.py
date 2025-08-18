from django.urls import path

from user.views import RequestOtpView, SignUpView, VerifyOtpView, UserInformationView, SignInView

urlpatterns = [
    path("api/v1/auth/otp/request/", RequestOtpView.as_view(), name='request-otp'),
    path("api/v1/auth/otp/verify/", VerifyOtpView.as_view(), name='verify_otp'),
    path("api/v1/auth/signup/", SignUpView.as_view(), name='signup'),
    path("api/v1/auth/signin/", SignInView.as_view(), name='signin'),

    path("api/v1/user/", UserInformationView.as_view(), name="user_information")
]
