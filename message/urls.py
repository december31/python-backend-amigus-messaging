from django.urls import re_path

from message.views import SendPrivateMessageView

urlpatterns = [
    re_path(r"api/v1/message/send/private?$", SendPrivateMessageView.as_view(), name="send_message"),
    re_path(r"api/v1/message/send/group?$", SendPrivateMessageView.as_view(), name="send_message"),
]
