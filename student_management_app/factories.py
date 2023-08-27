import factory
from faker import Factory
import datetime
import calendar
from django.utils import timezone
from . import models
import random
from django.db.models.signals import post_save

faker = Factory.create()


def randomDateOfThisYear():
    mth=random.randint(1,12)
    last_day=calendar.monthrange(datetime.date.today().year, mth)[1] # monthrange return weekday of first week and last day of the month
    day=random.randint(1,last_day)

    return datetime.date(datetime.date.today().year,mth,day)

@factory.django.mute_signals(post_save)
class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CustomUser
    
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    username = factory.Sequence(lambda x: f'{faker.first_name()}{x}')
    email = factory.Sequence(lambda x: f'{faker.first_name()}{faker.last_name()}{x}@gmail.com')
    password = 'pbkdf2_sha256$216000$iubvZkEUivjA$0fVu7T/t1AQeNX3q2ir7wbApdEPviI6QbvQEcVY0Jls='  # password
    date_joined = timezone.now()
    is_active = True
    
@factory.django.mute_signals(post_save)
class AdminUserFactory(CustomUserFactory):
    
    is_staff = True
    is_superuser = True
    user_type = models.CustomUser.HOD
    
@factory.django.mute_signals(post_save)
class StaffUserFactory(CustomUserFactory):

    is_staff = True
    user_type = models.CustomUser.STAFF

@factory.django.mute_signals(post_save)
class StudentsUserFactory(CustomUserFactory):

    user_type = models.CustomUser.STUDENT


@factory.django.mute_signals(post_save)
class AdminHODFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdminHOD
        
    admin = factory.SubFactory(AdminUserFactory)

@factory.django.mute_signals(post_save)
class StaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Staffs
                
    admin = factory.SubFactory(StaffUserFactory)
    address = factory.LazyAttribute(lambda _: faker.address())

    
class RelativeStaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RelativeStaff
    staff_id= factory.SubFactory(StaffFactory)
    name=factory.LazyAttribute(lambda _: faker.name())
    location=factory.LazyAttribute(lambda _: faker.city())
    age= random.randint(30,60)
    

class CoursesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Courses
        # django_get_or_create = ["course_name"]
    class Params:
        course="BCOM"

    course_name=factory.LazyAttribute(lambda x : x.course)
    # @factory.post_generation
    # def course_name(obj,create, extracted, **kwargs):
    #     if not create:
    #         return 
        

class SubjectsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subjects
        django_get_or_create = ["subject_name"]
    class Params:
        subject= "BK"

    subject_name=factory.LazyAttribute(lambda x : x.subject)
    course_id=factory.Iterator(models.Courses.objects.all())
    staff_id=factory.Iterator(models.CustomUser.objects.filter(user_type=models.CustomUser.STAFF))

class SessionYearModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model= models.SessionYearModel
        django_get_or_create=["session_start_year","session_end_year"]

    session_start_year=datetime.date(datetime.date.today().year, 1, 1)
    session_end_year=datetime.date(datetime.date.today().year, 12, 31)

    # @factory.post_generation
    # def session(obj,create,extracted, **kwargs):
    #     if not create:
    #         return
    #     from datetime import date
    #     start_year = date(date.today().year, 1, 1)
    #     end_year = date(date.today().year, 12, 31)
    #     session_year= models.SessionYearModel.objects.filter(
    #                                                     session_start_year=start_year,
    #                                                     session_end_year=end_year
    #                                                 )
    #     if not session_year:
    #         obj.session_start_year=start_year
    #         obj.session_end_year=end_year
    #     return
        

class StudentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Students

    admin=factory.SubFactory(StudentsUserFactory)
    gender=factory.Iterator(["Male","Female"])
    profile_pic="/FB_IMG_1462991253285.jpg"
    address=factory.LazyAttribute(lambda x: faker.address())
    course_id=factory.Iterator(models.Courses.objects.all())
    session_year_id=factory.Iterator(models.SessionYearModel.objects.filter(session_start_year=datetime.date(datetime.date.today().year, 1, 1)))

class AttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=models.Attendance

    subject_id=factory.Iterator(models.Subjects.objects.all())
    attendance_date=factory.LazyAttribute(lambda _: (datetime.datetime.today() - datetime.timedelta(days=random.randint(1,365))).date()) # generation random date but lesser then todays date   
    session_year_id=models.SessionYearModel.objects.get(session_start_year=datetime.date(datetime.date.today().year, 1, 1))

class AttendanceReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model =models.AttendanceReport

    student_id=factory.Iterator(models.Students.objects.all())
    attendance_id=factory.Iterator(models.Attendance.objects.all())
    status=factory.Iterator([0,1])

class LeaveReportStudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LeaveReportStudent

    student_id=factory.Iterator(models.Students.objects.all())
    leave_date=factory.LazyAttribute(lambda _: randomDateOfThisYear())
    leave_message=factory.Iterator(["Sick Leave","Vacation Leave","Birthday Leave"])
    leave_status=factory.Iterator([0,1])

class LeaveReportStaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LeaveReportStaff

    staff_id=factory.Iterator(models.Staffs.objects.all())
    leave_date=factory.LazyAttribute(lambda _: randomDateOfThisYear())
    leave_message=factory.Iterator(["Sick Leave","Vacation Leave","Birthday Leave"])
    leave_status=factory.Iterator([0,1])

class FeedBackStudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FeedBackStudent

    student_id=factory.Iterator(models.Students.objects.all())
    feedback=factory.Iterator(["Clean washroom everyday","Repair fan"])
    feedback_reply="Instruction pass to the peons"

class FeedBackStaffsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FeedBackStaffs
    staff_id=factory.Iterator(models.Staffs.objects.all())
    feedback=factory.Iterator(["Provide new chalk everyday in classwor,","clean staffroom"])
    feedback_reply="Instruction pass to the peons"
