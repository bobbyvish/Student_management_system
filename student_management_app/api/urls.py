from django.contrib import admin
from django.urls import path,include
from . import views, Hodviews
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"staffs", Hodviews.StaffViewSet, basename = 'staff')
router.register(r"all_users", Hodviews.AllUserViewSet, basename = 'all_users')
router.register(r"courses", Hodviews.CoursesViewSet, basename ="course")

urlpatterns = [
    path('', include(router.urls)),
    path("login", views.Login.as_view())

]