"""django import"""

"""model import"""


"""rest Framework import"""
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


"""serializer import"""
from . import serializers

from student_management_app.EmailBackEnd import EmailBackEnd
from . import helpers

class Login(APIView):

    def post(self, request):
        serializer = serializers.UserSerializer(data = request.data)
        if not serializer.is_valid():
            response = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "message" : "bad request",
                "data" : serializer.errors
            }
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        user = EmailBackEnd.authenticate(request, email = request.data.get('email') , password = request.data.get('password'))
        print(user)
        if not user:
            response = {
                "status" : status.HTTP_401_UNAUTHORIZED,
                "message" : "Invalid email or password",
                "data" : []
            }
            return Response(response, status = status.HTTP_400_BAD_REQUEST)

        token = helpers.get_tokens_for_user(user)
        response = {
            "status" : status.HTTP_200_OK,
            "message" : "Success",
            "data" : token
        }

        return Response(response, status = status.HTTP_200_OK)


