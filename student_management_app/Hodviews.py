from calendar import c
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .models import CustomUser,Courses, FeedBackStaffs, FeedBackStudent, LeaveReportStaff, LeaveReportStudent,Staffs,Subjects,Students,SessionYearModel,Attendance,AttendanceReport
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
from django.db.models import Max, F, OuterRef, Subquery, Prefetch, OuterRef, Count ,Q , Case , When ,Value , Sum
from django.db.models.functions import Coalesce

# from .models import RelativeStaff
# def AdminHomeTest(request):
#  
#     # from .models import RelativeStaff

#     """different query test"""
#     latest_leave_staff=LeaveReportStaff.objects.order_by('-created_at')
#     print("direct=================",latest_leave_staff)
#     staff_relative=RelativeStaff.objects.order_by('-created_at')
#     print("direct ralative============",staff_relative)

#     # latest_leave_staff=LeaveReportStaff.objects.annotate(max_date=Max('created_at')).filter(created_at=F('max_date'))
#     # print("direct=================",latest_leave_staff)
#     # staff_relative=RelativeStaff.objects.annotate(max_date=Max('created_at')).filter(created_at=F('max_date'))
#     # print("direct ralative============",staff_relative)

#     staffs=Staffs.objects.select_related("admin").prefetch_related(
#                                         Prefetch("leavereportstaff_set", queryset=latest_leave_staff , to_attr="leave_report")
#                                     ).prefetch_related(
#                                         Prefetch("relativestaff_set", queryset=staff_relative , to_attr="staff_relative")
#                                     )
#     for staff in staffs:
#         print(staff.leave_report)                               
#         print(staff.staff_relative)
#     total_staff=[]
#     for staff in staffs:
#         temp={}
#         temp["id"]=staff.id
#         temp["address"]=staff.address
#         temp["first_name"]=staff.admin.first_name
#         if staff.leave_report:
#             temp["leave_date"]=staff.leave_report[0].leave_date
#             temp["leave_message"]=staff.leave_report[0].leave_message

#         if staff.staff_relative:
#             temp["name"]=staff.staff_relative[0].name
#             temp["location"]=staff.staff_relative[0].location
#             temp["age"]=staff.staff_relative[0].age
#         total_staff.append(temp)
    
#     pprint(total_staff)
#     """proper woking code """
#     print("++++++++++++++++++++++++++++++++=======================================+++++++++++++++++++++++++++++++++")
#     """#1"""

#     latest_leave_staff=LeaveReportStaff.objects.annotate(max_date=Max('staff_id__leavereportstaff__created_at')).filter(created_at=F('max_date'))
#     # print("+++++++++++++++++++",latest_leave_staff)
#     staff_relative=RelativeStaff.objects.annotate(max_date=Max('staff_id__relativestaff__created_at')).filter(created_at=F('max_date'))
#     # print("++++++++++++++++++++++++++",staff_relative)
#     staffs=Staffs.objects.select_related("admin").prefetch_related(
#                                         Prefetch("leavereportstaff_set", queryset=latest_leave_staff , to_attr="leave_report")
#                                     ).prefetch_related(
#                                         Prefetch("relativestaff_set", queryset=staff_relative , to_attr="staff_relative")
#                                     )
#     for staff in staffs:
#         print(staff.leave_report)                               
#         print(staff.staff_relative)                               
#     total_staff=[]
#     for staff in staffs:
#         temp={}
#         temp["id"]=staff.id
#         temp["address"]=staff.address
#         temp["first_name"]=staff.admin.first_name
#         if staff.leave_report:
#             temp["leave_date"]=staff.leave_report[0].leave_date
#             temp["leave_message"]=staff.leave_report[0].leave_message

#         if staff.staff_relative:
#             temp["name"]=staff.staff_relative[0].name
#             temp["location"]=staff.staff_relative[0].location
#             temp["age"]=staff.staff_relative[0].age
#         total_staff.append(temp)

#     # print(total_staff)

#     """ #2 """
#     staff_data = Staffs.objects.all().select_related("admin").values("id","address","admin__first_name")
#     leave_staff=list(LeaveReportStaff.objects.filter(created_at__in=LeaveReportStaff.objects.values('staff_id_id').annotate(createds_at=Max('created_at')).values('createds_at')).values("id","staff_id_id","leave_date","leave_message","leave_status","created_at"))
#     staff_relative=list(RelativeStaff.objects.filter(created_at__in=RelativeStaff.objects.values('staff_id_id').annotate(createds_at=Max('created_at')).values('createds_at')).values("id","staff_id_id","name","location","age","created_at"))
#     # pprint(staff_data)
#     # pprint(leave_staff)

#     total_staff_using_for=[]

#     for staff in staff_data:
#         temp={}
#         temp["id"]=staff["id"]
#         temp["address"]=staff["address"]
#         temp["first_name"]=staff["admin__first_name"]
        
#         for leave in leave_staff:
#             # print(leave_staff)
#             if leave["staff_id_id"] == staff["id"]:
#                 temp["leave_date"]=leave["leave_date"]
#                 temp["leave_message"]=leave["leave_message"]
#                 leave_staff.remove(leave)
#                 break

#         for leave in staff_relative:
#             # print(staff_relative)
#             if leave["staff_id_id"] == staff["id"]:
#                 temp["name"]=leave["name"]
#                 temp["location"]=leave["location"]
#                 temp["age"]=leave["age"]
#                 staff_relative.remove(leave)
#                 break
                
#         total_staff_using_for.append(temp)

#     combine={
#         "total_staff_using_for" : total_staff_using_for,
#         "total_staff" : total_staff
#     }
#     # pprint(staff_data.values("leavereportstaff__leave_message"))

#     # return JsonResponse(combine, safe=False)
#     return render(request, 'hod_template/test.html')


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


def AddStaff(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))
    else:
        return render(request, 'hod_template/add_staff.html')
  
        

def AddCourse(request):
    if request.method == "POST":
        course = request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course added successfully")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed to Add Course")
            return HttpResponseRedirect(reverse("add_course"))
    else:
        return render(request, 'hod_template/add_course.html')


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

        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=3)
            user.students.address = address
            user.students.gender=gender
            user.students.profile_pic=profile_pic_url

            session_year=SessionYearModel.object.get(id=session_year_id)
            user.students.session_year_id = session_year
           
         
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.save()
            messages.success(request, "Successfully Added Student")
            return HttpResponseRedirect(reverse("add_student"))
        except:
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect(reverse("add_student"))
    else:
        course=Courses.objects.all()
        session_year=SessionYearModel.object.all()
        return render(request, 'hod_template/add_student.html',{"courses":course,"session_years":session_year})


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

            session_year=SessionYearModel.object.get(id=session_year_id)
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
        session_year=SessionYearModel.object.all()
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
    session_years=SessionYearModel.object.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_years":session_years})
    
@csrf_exempt
def Admin_Get_Attendance_Dates(request):
    subject=request.POST.get('subject')
    session_year_id=request.POST.get('session_year_id')
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
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
