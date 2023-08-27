import json
from calendar import c
from pprint import pprint
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, F, OuterRef, Subquery, Prefetch, OuterRef, Count ,Q , Case , When ,Value , Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.mixins import LoginRequiredMixin
from student_management_app.mixins import AdminRequiredMixin, StaffRequiredMixin
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from student_management_app.models import CustomUser,Courses, FeedBackStaffs, FeedBackStudent, LeaveReportStaff, LeaveReportStudent,Staffs,Subjects,Students,SessionYearModel,Attendance,AttendanceReport
from student_management_app.forms import StaffsForm, CoursesForm, StudentsForm, SubjectsForm
from student_management_system.services import UploadServices
from django.db import transaction

import logging
logger = logging.getLogger(__name__)


def AdminHome(request):

    total_courses=Courses.objects.annotate(
                                    subjects_count=Count("subjects"),
                                    students_count=Count("students")       
                                )
    
    # fetch courses and subjects 
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in total_courses:
        course_name_list.append(course.course_name)
        subject_count_list.append(course.subjects_count)
        student_count_list_in_course.append(course.students_count)

    # Fetch Subjects and total_students
    total_subjects=Subjects.objects.select_related("course_id").annotate(students_count=Count("course_id__students"))

    subject_list=[]
    student_count_list_in_subject=[]
    for subject in total_subjects:
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(subject.students_count)

    # prefetch_related(Prefetch("admin__subjects_set__attendance_set", queryset=Attendance.objects.count() ,to_attr="attendance"))
    # .prefetch_related(Prefetch("admin__subjects_set__attendance_set", queryset=Attendance.objects.filter(subject_id__staff_id=id) ,to_attr="atten"))

    total_staffs=Staffs.objects.select_related(
                                    "admin"
                                ).annotate(
                                    leaves=Count("leavereportstaff", filter=Q(leavereportstaff__leave_status=1)),
                                    attend=Count("admin__subjects__attendance")
                                ).order_by("attend")
    print(total_staffs)
    for i in total_staffs:
        print(i.admin.username,i.attend)
    total_staffs=Staffs.objects.all()

    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in total_staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    print(attendance_present_list_staff)
    print(attendance_absent_list_staff)
    print(staff_name_list)

    total_students=Students.objects.select_related("admin").prefetch_related(
                                        "attendancereport_set"
                                    ).values(
                                        "attendancereport__student_id"
                                    ).annotate(
                                        present=Count("attendancereport", filter=Q(attendancereport__status=True)),
                                        absent=Count("attendancereport", filter=Q(attendancereport__status=False)),
                                    ).values("attendancereport__student_id","admin__username","present", "absent")
    
    student_leaves=Students.objects.prefetch_related(
                                        "leavereportstudent_set"
                                    ).values(
                                        "leavereportstudent__student_id"
                                    ).annotate(
                                        leaves=Count("leavereportstudent", filter=Q(leavereportstudent__leave_status=1))
                                    )

    # print(student_leaves)

    # print(total_students)

    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in total_students:
        attendance_present_list_student.append(student["present"])
        attendance_absent_list_student.append(student["absent"])
        student_name_list.append(student["admin__username"])

    # print(attendance_present_list_student)
    # print(attendance_absent_list_student)
    # print(student_name_list)

    context={
        "students":total_students.count(),
        "staffs":total_staffs.count(),
        "subjects":total_subjects.count(),
        "courses":total_courses.count(),
        "course_name_list":course_name_list,
        "subject_count_list":subject_count_list,
        "student_count_list_in_course":student_count_list_in_course,
        "subject_list":subject_list,
        "student_count_list_in_subject":student_count_list_in_subject,
        "attendance_present_list_staff":attendance_present_list_staff,
        "attendance_absent_list_staff":attendance_absent_list_staff,
        "staff_name_list":staff_name_list,
        "attendance_present_list_student":attendance_present_list_student,
        "attendance_absent_list_student":attendance_absent_list_student,
        "student_name_list":student_name_list

    }
    return render(request, 'hod_template/home_content.html',context)


from django import forms
class CreateStaffView(LoginRequiredMixin,AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Staffs
    template_name = 'hod_template/add_staff.html'
    form_class = StaffsForm
    success_url = reverse_lazy("add_staff")
    success_message = "The staff member had been added successfully"

    def form_invalid(self, form):
        messages.error(self.request,form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except forms.ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)
        return response

    # def get(self,request):
    #     return render(request,self.template_name)
    
    # def post(self,request):
    #     form = self.form_class(request.POST)
    #     if not form.is_valid():
    #         messages.error(request, form.errors)
    #         return render(request,self.template_name)

    #     form.save()
    #     messages.success(request, "The staff member has been added successfully.")
    #     return HttpResponseRedirect(self.success_url)
    
class CreateCourseView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Courses
    # fields = ["course_name"]
    form_class = CoursesForm
    template_name = 'hod_template/add_course.html'
    success_url = reverse_lazy('add_course')
    success_message = "The course had been added successfully"


@transaction.atomic
def AddStudent(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        session_year_id = request.POST.get("session_year")
        gender= request.POST.get("gender")
        course_id= request.POST.get("course")
        profile_pic=request.FILES.get("profile_pic")

        # fs=FileSystemStorage()
        # filename=fs.save(profile_pic.name,profile_pic)
        # profile_pic_url=fs.url(filename)
        print("uplaod service is started")
                    
        allowed_type = ["image/jpeg","image/png"]
        allowed_extenstions = ["jpeg","jpg","png"]

        upload_service = UploadServices(allowed_type, allowed_extenstions)
        try:
            # Retrieve the SessionYearModel and Courses objects
            session_year=SessionYearModel.objects.get(id=session_year_id)
            course_obj = Courses.objects.get(id=course_id)
            
            # Wrap the database operations in a transaction.atomic() context manager
            with transaction.atomic():
                
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    last_name=last_name,
                    first_name=first_name,
                    user_type=3)
                user.students.address = address
                user.students.gender=gender
                
                user.students.session_year_id = session_year
                user.students.course_id = course_obj

                # Handle file upload using the UploadServices object
                try:
                    file_name = upload_service.upload(profile_pic,f"{first_name}{last_name}",Students.StudentFileUploadFolder)
                    logger.info(f"file_name is === {file_name}")
                except ValueError as e:
                    logger.error(str(e))
                    transaction.set_rollback(True)
                    messages.error(request, "Failed to uplaod file")
                    return HttpResponseRedirect(reverse("add_student"))
                except Exception as e:
                    logger.error(str(e))
                    transaction.set_rollback(True)
                    messages.error(request, "Failed to uplaod file")
                    return HttpResponseRedirect(reverse("add_student"))
                
                # Update the student's profile pic
                logger.debug("Updating Student profile pix")
                user.students.profile_pic=file_name
                user.save()
                
                # If everything is successful, redirect to the add_student page with success message
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
        except Exception as e:
            logger.error(str(e))
            # Rollback the transaction in case of any exception
            transaction.set_rollback(True)
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect(reverse("add_student"))
    else:
        # Retrieve all the courses and session years to be passed to the template
        course=Courses.objects.all()
        session_year=SessionYearModel.objects.all()
        return render(request, 'hod_template/add_student.html',{"courses":course,"session_years":session_year})


class CreateSubjectView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Subjects
    form_class = SubjectsForm
    template_name = "hod_template/add_subject.html"
    success_url = reverse_lazy("add_subject")
    success_message = "The subject had been added successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses=Courses.objects.all()
        staffs=CustomUser.objects.filter(user_type=2)
        context["courses"] = courses
        context["staffs"] = staffs
        logger.debug(f"context {context}")
        return context
    
    def form_invalid(self, form):
        messages.error(self.request,form.errors)
        return super().form_invalid(form)  

def AddSubject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject")
        course_id = request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)
        
        try:
            subject =Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))
    else:
        courses=Courses.objects.all()
        staffs=CustomUser.objects.filter(user_type=2)
        return render(request,"hod_template/add_subject.html",{"courses":courses,"staffs":staffs})


def ManageStaff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs})

def ManageStudent(request):
    students=Students.objects.all()
    return render(request,"hod_template/manage_student.html",{"students":students})


def ManageCourse(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course.html",{"courses":courses})

def ManageSubject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject.html",{'subjects':subjects})

def EditStaff(request,staff_id):
    if request.method == "POST":
        print(staff_id)
        # staff_id=request.POST.get('staff_id')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.username=username
            user.email=email
            user.last_name=last_name
            user.first_name=first_name
            user.save()

            staff_obj=Staffs.objects.get(admin=staff_id)
            staff_obj.address=address
            staff_obj.save()
            messages.success(request, "Successfully Updated Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request, "Failed to Update Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
    else:
        staff=Staffs.objects.get(admin=staff_id)
        return render(request,'hod_template/edit_staff.html',{'staff':staff,'id':staff_id})


def EditStudent(request, student_id):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        session_year_id = request.POST.get("session_year")
        gender= request.POST.get("gender")
        course_id= request.POST.get("course")

        if request.FILES.get("profile_pic",False):
            profile_pic=request.FILES.get("profile_pic")

            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
        else:
            profile_pic_url=None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.username=username
            user.email=email
            user.last_name=last_name
            user.first_name=first_name
            user.save()

            student=Students.objects.get(admin=student_id)
            student.address=address
            student.gender=gender
            if profile_pic_url !=None:
                student.profile_pic=profile_pic_url

            session_year=SessionYearModel.objects.get(id=session_year_id)
            student.session_year_id=session_year

            course_obj = Courses.objects.get(id=course_id)
            student.course_id = course_obj
            student.save()
            messages.success(request, "Successfully Updated Student")
            return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        except:
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
    else:
        course=Courses.objects.all()
        student=Students.objects.get(admin=student_id)
        session_year=SessionYearModel.objects.all()
        return render(request, 'hod_template/edit_student.html',{"courses":course,"student":student,"session_years":session_year,"id":student_id})


def EditSubject(request,subject_id):
    if request.method == "POST":
        subject_name = request.POST.get("subject")
        course_id = request.POST.get("course")
        staff_id = request.POST.get("staff")

        try:
            subject =Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name

            course=Courses.objects.get(id=course_id)
            subject.course_id=course
        
            staff=CustomUser.objects.get(id=staff_id)   
            subject.staff_id=staff
            subject.save()
            messages.success(request, "Successfully Updated Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request, "Failed to Update Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
    else:
        subject=Subjects.objects.get(id=subject_id)
        courses=Courses.objects.all()
        staffs=CustomUser.objects.filter(user_type=2)
        return render(request,"hod_template/edit_subject.html",{"subject":subject,"courses":courses,"staffs":staffs ,"id":subject_id})



def EditCourse(request, course_id):
    if request.method == "POST":
        course = request.POST.get("course")
        try:
            course_obj=Courses.objects.get(id=course_id)
            course_obj.course_name=course
            course_obj.save()
            messages.success(request, "Course Updated successfully")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request, "Failed to Update Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
    else:
        course=Courses.objects.get(id=course_id)
        return render(request, 'hod_template/edit_course.html',{"course":course,'id':course_id})



def ManageSession_Year(request):
    if request.method == 'POST':
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")
        try:
            session=SessionYearModel(
                session_start_year=session_start_year,
                session_end_year=session_end_year
            )
            session.save()
            messages.success(request, "Session Year Added successfully")
            return HttpResponseRedirect(reverse("manage_session"))
        
        except:
            messages.success(request, "Failed to Add Session Year")
            return HttpResponseRedirect(reverse("manage_session"))
    return render(request, 'hod_template/manage_session_year.html')

@csrf_exempt
def Student_Feedback_Message(request):
    if request.method == "POST":
        feedback_id=request.POST.get("id")
        feedback_message=request.POST.get("message")
        try:
            feedback=FeedBackStudent.objects.get(id=feedback_id)
            feedback.feedback_reply=feedback_message
            feedback.save()
            return HttpResponse("True")
        except:
            return HttpResponse("False")
    else:
        feedbacks=FeedBackStudent.objects.all()
        return render(request,'hod_template/reply_feedback_tostudent.html',{"feedbacks":feedbacks})

@csrf_exempt
def Staff_Feedback_Message(request):
    if request.method == "POST":
        feedback_id=request.POST.get("id")
        feedback_message=request.POST.get("message")
        try:
            feedback=FeedBackStaffs.objects.get(id=feedback_id)
            feedback.feedback_reply=feedback_message
            feedback.save()
            return HttpResponse("True")
        except:
            return HttpResponse("False")
    else:
        feedbacks=FeedBackStaffs.objects.all()
        return render(request,'hod_template/reply_feedback_tostaff.html',{"feedbacks":feedbacks})


def Student_Leave(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_report.html",{"leaves":leaves})
    

def Staff_Leave(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"hod_template/staff_leave_report.html",{"leaves":leaves})
    


def Student_Leave_Action(request,leave_id,action):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    if action=='yes':
        leave.leave_status=1
    else:
        leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse('student_leave_report'))

def Staff_Leave_Action(request,leave_id,action):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    if action=='yes':
        leave.leave_status=1
    else:
        leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse('staff_leave_report'))

def Admin_View_Attendance(request):
    subjects=Subjects.objects.all()
    session_years=SessionYearModel.objectss.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_years":session_years})
    
@csrf_exempt
def Admin_Get_Attendance_Dates(request):
    subject=request.POST.get('subject')
    session_year_id=request.POST.get('session_year_id')
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def Admin_Get_Attendance_Student(request):
    attendance_date=request.POST.get('attendance_date')
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)   
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def Admin_Profile(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse('admin_profile'))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse('admin_profile'))
    else:
        user=CustomUser.objects.get(id=request.user.id)
        return render(request, 'hod_template/admin_profile.html',{"user":user})
