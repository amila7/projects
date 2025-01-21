from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class HelloView(APIView):
    def get(self, request, *args, **kwargs): 
        data = {
            "user_name": "admin",
            "message": "Hello World!"
        }
        return Response(data)
