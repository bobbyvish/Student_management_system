from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import CustomUser,Students,Courses,Staffs, Subjects,SessionYearModel,Attendance,AttendanceReport,LeaveReportStaff,FeedBackStaffs,StudentResult
import json
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
# from django.core import serializers


def StaffHome(request):
    # for fetch all student under staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    total_subjects=subjects.count()
    
    # Fetch all approve leave              
    staff=Staffs.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()

    # fetch all course of user staf
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        if course not in course_id_list:
            course_id_list.append(course)

     #fetch all Attendance Count
    total_attendance=Attendance.objects.filter(subject_id__in=subjects).count

    # fetch attendance data by subjects
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count)

    students=Students.objects.filter(course_id__in=course_id_list)
    students_count=students.count()
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)


    context={
        "total_subjects":total_subjects,
        "leave_count":leave_count,
        "students":students_count,
        "total_attendance":total_attendance,
        "subject_list":subject_list,
        "attendance_list":attendance_list,
        "student_list":student_list,
        "student_list_attendance_present":student_list_attendance_present,
        "student_list_attendance_absent":student_list_attendance_absent
    }
    return render(request,"staff_template/staff_home_template.html",context)

def Staff_Take_Attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def Get_Students(request):
    subject_id=request.POST.get('subject')
    session_year=request.POST.get('session_year')
    subject=Subjects.objects.get(id=subject_id)
    session_year_obj=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_year_obj)
    
    # student_data=serializers.serialize("python",students)
    student_data=[]
    for student in students:
        small_data={"id":student.admin.id,"name":student.admin.first_name +" "+ student.admin.last_name}
        student_data.append(small_data)
    return JsonResponse(json.dumps(student_data),content_type="application/json",safe=False)

@csrf_exempt
def Save_Attendance_Data(request):
    student_ids=request.POST.get('student_ids')
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")
    print(student_ids)
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_student=json.loads(student_ids)
    try:
        attendance=Attendance(
            subject_id=subject_model,
            attendance_date=attendance_date,
            session_year_id=session_model)
        attendance.save()

        for stud in json_student:
            student=Students.objects.get(admin=stud['id'])
            attendance_report=AttendanceReport(
                               student_id=student,
                               attendance_id=attendance,
                               status=stud['status']
                            )
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def Staff_Update_Attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_years":session_years})
    
@csrf_exempt
def Get_Attendance_dates(request):
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
def Get_Attendance_student(request):
    attendance_date=request.POST.get('attendance_date')
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)   
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def Update_Attendance_Data(request):
    student_ids=request.POST.get('student_ids')
    attendance_date=request.POST.get("attendance_date")
    print(student_ids)

    attendance=Attendance.objects.get(id=attendance_date)

    json_student=json.loads(student_ids)
    try:
        
        for stud in json_student:
            student=Students.objects.get(admin=stud['id'])
            attendance_report=AttendanceReport.objects.get(
                               student_id=student,
                               attendance_id=attendance
                            )
            attendance_report.status=stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def Staff_Apply_Leave(request):
    staff_obj=Staffs.objects.get(admin=request.user.id)
    if request.method == "POST":
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")
        try:
            leave_report=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg)
            leave_report.save()
            messages.success(request,"Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.success(request,"Failed to apply Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))

    else:
        leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
        return render(request,"staff_template/staff_apply_leave.html",{"leave_data":leave_data})

def Staff_Feedback(request):
    staff_id=Staffs.objects.get(admin=request.user.id)
    if request.method == "POST":
        feedback_msg=request.POST.get("feedback_msg")
        try:
            feedback=FeedBackStaffs(staff_id=staff_id, feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request,"Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.success(request,"Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data": feedback_data})

def Staff_Profile(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')
        address=request.POST.get('address')
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse('staff_profile'))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse('staff_profile'))
    else:
        user=CustomUser.objects.get(id=request.user.id)
        staff=Staffs.objects.get(admin=user)
        return render(request, 'staff_template/staff_profile.html',{"user":user,'staff':staff})



def Staff_Add_Result(request):
    if request.method == "POST":
        student_admin_id=request.POST.get('student_list')
        assignment_marks=request.POST.get('assignment_marks')
        exam_marks=request.POST.get('exam_marks')
        subject_id=request.POST.get('subject')


        student_obj=Students.objects.get(admin=student_admin_id)
        subject_obj=Subjects.objects.get(id=subject_id)

        try:
            check_exist=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
            if check_exist:
                result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
                result.subject_assignment_marks=assignment_marks
                result.subject_exam_marks=exam_marks
                result.save()
                messages.success(request, "Successfully Updated Result")
                return HttpResponseRedirect(reverse("staff_add_result"))
            else:
                result=StudentResult(student_id=student_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Successfully Added Result")
                return HttpResponseRedirect(reverse("staff_add_result"))
        except:
            messages.error(request, "Failed to Add Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
    else:
        subjects=Subjects.objects.filter(staff_id=request.user.id)
        session_years=SessionYearModel.object.all()
        return render(request,"staff_template/staff_add_result.html",{"subjects":subjects,"session_years":session_years})
 

def Staff_Edit_Result(request):
    if request.method == "POST":
        subject_id=request.POST.get('subject')
        student_id=request.POST.get('student')
        assignment_marks=request.POST.get('assignment_marks')
        exam_marks=request.POST.get('exam_marks')

        student_obj = Students.objects.get(admin=student_id)
        subject_obj = Subjects.objects.get(id=subject_id)
        result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
        result.subject_assignment_marks=assignment_marks
        result.subject_exam_marks=exam_marks
        result.save()
        messages.success(request, "Successfully Updated Result")
        return HttpResponseRedirect(reverse("staff_edit_result"))
    else:
        subjects=Subjects.objects.filter(staff_id=request.user.id)
        session_years=SessionYearModel.object.all()
        return render(request,"staff_template/staff_edit_result.html",{"subjects":subjects,"session_years":session_years})
 
@csrf_exempt
def Fetch_Result_Student(request):
    subject_id=request.POST.get('subject_id')
    student_id=request.POST.get('student_id')
    student_obj=Students.objects.get(admin=student_id)
    result=StudentResult.objects.filter(student_id=student_obj.id,subject_id=subject_id).exists()
    if result:
        result=StudentResult.objects.get(student_id=student_obj.id,subject_id=subject_id)
        result_data={"exam_marks":result.subject_exam_marks,"assign_marks":result.subject_assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")