"""django import"""

"""model import"""
from student_management_app import models

"""rest Framework import"""
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets


"""serializer import"""
from . import serializers


"""filter import"""
from django_filters.rest_framework import DjangoFilterBackend
from student_management_app import filters


class AllUserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomUserSerializer
    queryset = models.CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.CustomUserFilter

class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StaffsSerializer
    queryset = models.Staffs.objects.select_related("admin").all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.StaffsFilter

class CoursesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CoursesSerializer
    queryset = models.Courses.objects.all()
    filter_backends =[DjangoFilterBackend]
    filterset_class = filters.CoursesFilter

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentsSerializer
    queryset = models.Students.objects.all()
    