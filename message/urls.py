from django.urls import re_path

from message.views import (
    GroupMessageView,
    PrivateMessageView,
    SendPrivateMessageView,
    RecentMessagesView,
)

urlpatterns = [
    re_path(
        r"api/v1/message/send/private/?$",
        SendPrivateMessageView.as_view(),
        name="send_message",
    ),
    re_path(
        r"api/v1/message/send/group/?$",
        SendPrivateMessageView.as_view(),
        name="send_message",
    ),
    re_path(
        r"api/v1/message/recent/?$",
        RecentMessagesView.as_view(),
        name="recent_messages",
    ),
    re_path(
        r"api/v1/message/private/?$",
        PrivateMessageView.as_view(),
        name="private_messages",
    ),
    re_path(
        r"api/v1/message/group/?$", GroupMessageView.as_view(), name="group_messages"
    ),
]
