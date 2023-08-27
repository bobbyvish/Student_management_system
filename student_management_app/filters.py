import django_filters
from . import models


class CustomUserFilter(django_filters.FilterSet):
    user_type = django_filters.ChoiceFilter(choices=models.CustomUser.user_type_data)

    class Meta:
        model = models.CustomUser
        fields ={
            'username': ["exact", "icontains"],
            'email' : ["exact", "icontains"],
            'date_joined': ["exact", "gte","lte"],
        }

class StaffsFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name = "admin__username", lookup_expr="icontains")
    first_name = django_filters.CharFilter(field_name = "admin__first_name", lookup_expr="icontains")
    last_name = django_filters.CharFilter(field_name = "admin__last_name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name = "admin__email", lookup_expr="icontains")
    address = django_filters.CharFilter(field_name = "address", lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter(field_name = "created_at")
    
    class Meta:
        model= models.Staffs
        fields =[
            "username",
            "first_name",
            "last_name",
            "email",
            "address",
            "created_at",
        ]


class CoursesFilter(django_filters.FilterSet):
    course_name = django_filters.ModelChoiceFilter(
        field_name='course_name',
        queryset=models.Courses.objects.all().values_list("course_name", flat=True),
        label='Course Name'
    )
    class Meta:
        model = models.Courses
        # fields = {
        #     "course_name" : ["icontains"]
        # }
        fields = ['course_name']

