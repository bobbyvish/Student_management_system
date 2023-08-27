from django import forms
from . import models
from django.db import transaction

# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         model = models.CustomUser
#         fields = [
#             "first_name",
#             "last_name",
#             "username",
#             "email",
#             "password",
#             "user_type"
#         ]

class CustomUserForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=100)
    

class StaffsForm(CustomUserForm, forms.ModelForm):
    address = forms.CharField(label='Address', max_length=100)
    
    class Meta:
        model = models.Staffs
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "address"
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user=models.CustomUser.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    @transaction.atomic()
    def save(self, commit=True):
        try:
            with transaction.atomic():
                user = models.CustomUser.objects.create_user(
                    user_type=models.CustomUser.STAFF,
                    username=self.cleaned_data['username'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    email=self.cleaned_data['email'],
                    password=self.cleaned_data['password']
                )
                staff, created = models.Staffs.objects.get_or_create(admin=user)
                staff.address = self.cleaned_data['address']
                staff.save()
        except Exception as e:
            print(e)
            transaction.set_rollback(True)
            raise forms.ValidationError("Failed to Add Staff")
        # user = super().save(commit=False)
        # user.user_type = models.CustomUser.STAFF
        # user.save()
        # staff, created = models.Staffs.objects.get_or_create(admin=user)
        # staff.address = self.cleaned_data['address']
        # staff.save()
        # return staff

class StudentsForm(CustomUserForm, forms.ModelForm):
    address = forms.CharField(label='Address', max_length=100)
    class Meta:
        model = models.Students
        exclude = [
            "fcm_token"
        ]

class CoursesForm(forms.ModelForm):
    class Meta:
        model = models.Courses
        fields = "__all__"

class SubjectsForm(forms.ModelForm):
    class Meta:
        model = models.Subjects
        fields = "__all__"

    def save(self, commit=True):
        # subject_name = self.cleaned_data.get("subject")
        # course_id = self.cleaned_data.get("course")
        # course= models.Courses.objects.get(id=course_id)
        # staff_id = self.cleaned_data.get("staff")
        # staff= models.CustomUser.objects.get(id=staff_id)
        # subject = models.Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
        # subject.save()
        subject = super().save(commit=False)
        course_id = self.cleaned_data.get("course")
        staff_id = self.cleaned_data.get("staff")
        course = models.Courses.objects.get(id=course_id)
        staff = models.CustomUser.objects.get(id=staff_id)
        subject.course = course
        subject.staff = staff
        if commit:
            subject.save()
        return subject

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = models.Attendance
        fields = "__all__"

class AttendanceReportForm(forms.ModelForm):
    class Meta:
        model = models.AttendanceReport
        fields = "__all__"

class LeaveReportStudentForm(forms.ModelForm):
    class Meta:
        model = models.LeaveReportStudent
        fields = "__all__"

class LeaveReportStaffForm(forms.ModelForm):
    class Meta:
        model = models.LeaveReportStaff
        fields = "__all__"

class FeedBackStudentForm(forms.ModelForm):
    class Meta:
        model = models.FeedBackStudent
        fields = "__all__"

class FeedBackStaffForm(forms.ModelForm):
    class Meta:
        model = models.FeedBackStaffs
        fields = "__all__"
