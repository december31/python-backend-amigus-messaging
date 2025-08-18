from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView


# Create your views here.

class BaseRetrieveApiView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        pass
