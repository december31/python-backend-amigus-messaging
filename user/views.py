import logging
import random
import time

from django.core.mail import send_mail
from django.db.models import Subquery
from drf_spectacular.utils import extend_schema, OpenApiParameter
from kombu.pools import get_limit
from rest_framework import views, serializers, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from base.response import (
    BaseResponse,
    too_many_request,
    success,
    internal_server_error,
    user_not_found, otp_is_not_correct, otp_has_expired, otp_has_not_been_requested, email_already_registered, email_field_is_incorrect,
    phone_field_is_incorrect, phone_already_registered, password_is_incorrect, account_does_not_existed, BaseListResponse,
)
from message.models import Conversation, ConversationParticipant
from project import settings
from user.models import User, Token
from user.serializers import (
    OTPRequestSerializer,
    SignUpSerializer,
    VerifyOtpSerializer,
    TokenSerializer,
    UserSerializer,
    SignInSerializer, UpdateUserInformationSerializer, ChangePasswordSerializer,
)
from utils.base_exception import BaseApiException
from utils.model_utils import get_object_or_exception
from utils.otp import (
    get_otp_requested_timestamp,
    set_otp,
    set_otp_requested_timestamp,
    get_otp,
)
from utils.tokens import generate_token

logger = logging.getLogger(__name__)

# Define constants (can also be in settings.py)
OTP_EXPIRY_SECONDS = getattr(settings, "OTP_EXPIRY_SECONDS", 300)  # 5 minutes
OTP_LENGTH = getattr(settings, "OTP_LENGTH", 6)
OTP_RATE_LIMIT_SECONDS = getattr(settings, "OTP_RATE_LIMIT_SECONDS", 60)  # 1 minute


class RequestOtpView(views.APIView):
    serializer_class = OTPRequestSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    @extend_schema(
        tags=["Auth"],
        summary="Request otp for verification",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data["identifier"]

        last_requested_time = get_otp_requested_timestamp(identifier)
        if (
            last_requested_time
            and time.time() - last_requested_time < OTP_RATE_LIMIT_SECONDS
        ):
            logger.warning(f"Rate limit exceeded for identifier: {identifier}")
            return BaseResponse.create(too_many_request)

        otp_code = "".join(random.choices("0123456789", k=OTP_LENGTH))

        set_otp(identifier, otp_code)
        set_otp_requested_timestamp(identifier, time.time())

        try:
            if "@" in identifier:
                self._send_otp_via_email(identifier, otp_code)
                message = f"OTP sent to email: {identifier}. Valid for {OTP_EXPIRY_SECONDS / 60} minutes."
            else:
                self._send_otp_via_email(identifier, otp_code)
                message = f"OTP sent to phone: {identifier}. Valid for {OTP_EXPIRY_SECONDS / 60} minutes."
            logger.info(
                f"OTP ({otp_code}) successfully generated and simulated sending to {identifier}"
            )
            return BaseResponse.create(http_status=success, message=message, data={})
        except Exception as e:
            logger.error(f"Error sending OTP to {identifier}: {e}", exc_info=True)
            return BaseResponse.create(
                http_status=internal_server_error,
                message="Failed to send OTP. Please try again.",
            )

    @staticmethod
    def _send_otp_via_email(identifier, otp_code):
        send_mail(
            "Cambot One Time Password",
            f"Your one time password is {otp_code}",
            "ducangt3112@gmail.com",
            [identifier],
            fail_silently=False,
        )

    def _send_otp_via_sms(self, identifier, otp_code):
        pass


class VerifyOtpView(views.APIView):
    serializer_class = VerifyOtpSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    @extend_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]

        otp_requested_timestamp = get_otp_requested_timestamp(identifier)

        if not otp_requested_timestamp:
            return BaseResponse.create(http_status=otp_has_not_been_requested)

        if time.time() - otp_requested_timestamp > OTP_EXPIRY_SECONDS:
            return BaseResponse.create(http_status=otp_has_expired)

        otp = get_otp(identifier)

        if otp != serializer.validated_data["otp"]:
            return BaseResponse.create(http_status=otp_is_not_correct)

        set_otp(identifier, None)
        set_otp_requested_timestamp(identifier, None)

        if "@" in identifier:
            user = User.objects.get_by_email_or_null(email=identifier)
            if not user:
                user = User.objects.create(email=identifier, username=identifier)
        else:
            user = User.objects.get_by_phone_or_null(phone=identifier)
            if not user:
                user = User.objects.create(phone=identifier, username=identifier)

        access_token, refresh_token = generate_token(user)

        token = Token.objects.create(
            access_token=access_token, refresh_token=refresh_token, owner=user, is_one_time_token=True
        )

        return BaseResponse.create(
            http_status=success, data={
                "one_time_token": token.access_token
            }
        )


class SignUpView(views.APIView):
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        sign_up_data = SignUpSerializer(data=request.data)
        sign_up_data.is_valid(raise_exception=True)

        identifier = sign_up_data.data.get("identifier")
        password = sign_up_data.data.get("password")

        user = request.user

        print(identifier)
        print(user.email)

        if "@" in identifier:
            email = identifier
            if email and user.email and user.email != email:
                raise BaseApiException.create(email_field_is_incorrect)
            elif user.is_initialized:
                raise BaseApiException.create(email_already_registered)
            user.email = email

        else:
            phone = identifier
            if phone and user.phone and user.phone != phone:
                raise BaseApiException.create(phone_field_is_incorrect)
            elif user.is_initialized:
                raise BaseApiException.create(phone_already_registered)
            user.phone = phone

        user.is_initialized = True
        user.set_password(password)
        user.save()

        return BaseResponse.create(http_status=success, data=UserSerializer(user).data)


class SignInAccountView(views.APIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    @extend_schema(tags=["Auth"])
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data.get("identifier")
        password = serializer.validated_data.get("password")

        if "@" in identifier:
            user = User.objects.get_by_email_or_null(email=identifier)
        else:
            user = User.objects.get_by_phone_or_null(phone=identifier)

        if user is None:
            raise BaseApiException.create(account_does_not_existed)

        if not user.check_password(password):
            raise BaseApiException.create(password_is_incorrect)

        access_token, refresh_token = generate_token(user)

        token = Token.objects.create(
            access_token=access_token, refresh_token=refresh_token, owner=user
        )

        return BaseResponse.create(
            http_status=success, data=TokenSerializer(token).data
        )


class ChangePasswordView(views.APIView):
    serializer_class = ChangePasswordSerializer

    @extend_schema(tags=["Auth"])
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data.get("identifier")
        password = serializer.validated_data.get("password")

        if "@" in identifier:
            user = User.objects.get_by_email_or_null(email=identifier)
        else:
            user = User.objects.get_by_phone_or_null(phone=identifier)

        if user is None:
            raise BaseApiException.create(account_does_not_existed)

        user.set_password(password)
        user.save()

        return BaseResponse.create(http_status=success, data=UserSerializer(user).data)


class PersonalInformationView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            return UpdateUserInformationSerializer
        else:
            return UserSerializer

    @extend_schema(tags=["User"])
    def get(self, request):
        return BaseResponse.create(http_status=success, data=UserSerializer(request.user).data)

    @extend_schema(tags=["User"])
    def put(self, request, *args, **kwargs):
        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user.email = serializer.validated_data["email"]
        user.phone = serializer.validated_data["phone"]
        user.display_name = serializer.validated_data["display_name"]
        user.save()

        return BaseResponse.create(http_status=success, data=serializer.data)

    @extend_schema(tags=["User"])
    def patch(self, request, *args, **kwargs):
        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone = serializer.validated_data.get("phone")

        if email:
            user.email = serializer.validated_data["email"]

        if phone:
            user.phone = serializer.validated_data["phone"]

        user.save()

        return BaseResponse.create(http_status=success, data=serializer.data)


class UserInformationView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["User"],
        parameters=[
            OpenApiParameter(name="id", type=int, required=False, description="User ID"),
            OpenApiParameter(name="email", type=str, required=False, description="User Email"),
            OpenApiParameter(name="phone", type=str, required=False, description="User Phone")
        ]
    )
    def get(self, request):
        user_id = request.query_params.get("id")
        user_email = request.query_params.get("email")
        user_phone = request.query_params.get("phone")
        if user_id:
            user = get_object_or_exception(User.objects, user_not_found, id=user_id)
        elif user_email:
            user = get_object_or_exception(User.objects, user_not_found, email=user_email)
        elif user_phone:
            user = get_object_or_exception(User.objects, user_not_found, phone=user_phone)
        else:
            raise BaseApiException.create(user_not_found)

        return BaseListResponse.create(http_status=success, data=UserSerializer(user).data)


class ContactsView(views.APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Contacts"],
        parameters=[
            OpenApiParameter(name="limit", type=int, description="Number of contacts to return"),
            OpenApiParameter(name="offset", type=int, description="Number of contacts to ignored")
        ])
    def get(self, request):
        if self.get_limit(request) <= 0:
            return BaseListResponse.create(success, data=[])
        if self.get_offset(request) < 0:
            return BaseListResponse.create(success, data=[])

        conversation_participants = User.objects.filter(
            id__in=ConversationParticipant.objects.filter(
                conversation__id__in=Conversation.objects.filter(
                    participants__user__id__in=[request.user.id],
                    type=Conversation.TypeChoice.PRIVATE.value
                ).values("id")
            ).exclude(user__id=request.user.id).values_list("user")
        ).order_by("display_name", "email", "phone")

        result = self.paginate_queryset(conversation_participants, request, view=self)

        return BaseListResponse.create(success, data=UserSerializer(result, many=True).data)
