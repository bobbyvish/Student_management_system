"""django import"""
from django.contrib.auth import get_user_model


"""rest framework import"""
from rest_framework import serializers, validators

from student_management_app import models


UserModel = get_user_model()

# class ChoiceField(serializers.ChoiceField):

#     def to_representation(self, obj):
#         if obj == '' and self.allow_blank:
#             return obj
#         return self._choices[obj]

#     def to_internal_value(self, data):
#         # To support inserts with the value
#         if data == '' and self.allow_blank:
#             return ''

#         for key, val in self._choices.items():
#             if val == data:
#                 return key
#         self.fail('invalid_choice', input=data)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = [
            "email",
            "password"
        ]
        extra_kwargs = {
            'email' :{'required': True},
            'password' :{'required': True}
        }

class CustomUserSerializer(serializers.ModelSerializer):
    email =  serializers.EmailField(
                            validators=[
                                    validators.UniqueValidator(
                                            queryset=models.CustomUser.objects.all()
                                    )
                            ]
                        )
    user_type = serializers.CharField(source='get_user_type_display')

    class Meta:
        model = models.CustomUser
        fields = [
            "id",
            "user_type",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "date_joined"
        ]
        write_only_fields = ["password"]
        read_only_fields = ["id","date_joined"]

class AdminHODSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminHOD
        fields = serializers.ALL_FIELDS
        depth = 1

class StaffsSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(read_only=True)
    admin = CustomUserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = models.Staffs
        exclude = ["updated_at","fcm_token"]
        depth = 1

    def create(self, validated_data):
        print(validated_data)
        address = validated_data.pop("address")
        user = models.CustomUser.objects.create_user(**validated_data)
        staff = models.Staffs.objects.create(admin=user, address=address)
        return staff
    
    def update(self, instance, validated_data):
        instance.admin.first_name = validated_data.get('first_name',instance.admin.first_name)
        instance.admin.last_name = validated_data.get('last_name',instance.admin.last_name)
        instance.admin.username = validated_data.get('username',instance.admin.username)
        instance.admin.save()
        instance.address = validated_data.get('address',instance.address)
        instance.save()
        return instance

class RelativeStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RelativeStaff
        fields = serializers.ALL_FIELDS
        depth =1 

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Courses
        fields = serializers.ALL_FIELDS


class SubjectsSerializer(serializers.ModelSerializer):
    course_id=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = models.Subjects
        fields = serializers.ALL_FIELDS


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Students
        fields = serializers.ALL_FIELDS
        depth = 1