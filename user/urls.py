from django.urls import path
from user.views import Test

urlpatterns = [
    path('api/test/', Test.as_view(), name='test')
]
