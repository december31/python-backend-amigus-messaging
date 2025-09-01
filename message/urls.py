from django.urls import re_path

from message.views import SendPrivateMessageView

urlpatterns = [
    re_path(r"api/v1/message/send/?$", SendPrivateMessageView.as_view(), name="send_message"),
]
