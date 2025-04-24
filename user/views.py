from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from base.response import BaseResponse, BaseListResponse

from base.status import success


# Create your views here.


class Test(APIView):
    def get(self, request):
        return BaseListResponse.create(http_status=success, data=['hello'], page=0, page_size=1)
