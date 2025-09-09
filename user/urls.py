from django.urls import re_path

from user.views import RequestOtpView, SignUpView, VerifyOtpView, UserInformationView, SignInAccountView, ChangePasswordView, PersonalInformationView, \
    ContactsView

urlpatterns = [
    re_path(r"^api/v1/auth/otp/request/?$", RequestOtpView.as_view(), name='request-otp'),
    re_path(r"^api/v1/auth/otp/verify/?$", VerifyOtpView.as_view(), name='verify_otp'),
    re_path(r"^api/v1/auth/sign-up/?$", SignUpView.as_view(), name='signup'),
    re_path(r"^api/v1/auth/sign-in/account/?$", SignInAccountView.as_view(), name='signin'),
    re_path(r"^api/v1/auth/change-password/?$", ChangePasswordView.as_view(), name='change_password'),

    re_path(r"^api/v1/user/?$", UserInformationView.as_view(), name="user_information"),
    re_path(r"^api/v1/user/me/?$", PersonalInformationView.as_view(), name="personal_information"),

    re_path(r"^api/v1/contact/?$", ContactsView.as_view(), name="contacts")
]

