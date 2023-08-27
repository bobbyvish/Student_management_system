from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from student_management_app.models import CustomUser ,Students,Subjects,Courses,Attendance,AttendanceReport,LeaveReportStudent,FeedBackStudent,LeaveReportStudent,StudentResult
import datetime
from django.core import serializers


def StudentHome(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course_id.id)
    subjects=Subjects.objects.filter(course_id=course).count()

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance=Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)        





    context={
        "total_attendance":attendance_total,
        "attendance_absent":attendance_absent,
        "attendance_present":attendance_present,
        "subject":subjects,
        "data_name":subject_name,
        "data1_present":data_present,
        "data2_absent":data_absent,
    }

    return render(request,"student_template/student_home_template.html",context)

@csrf_exempt
def Student_View_Attendance(request):
    if request.method == "POST":
        subject_id=request.POST.get("subject")
        start_date=request.POST.get("start_date")
        end_date=request.POST.get("end_date")
        
        start_date_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
        

        subject_obj=Subjects.objects.get(id=subject_id)
        stud_obj=Students.objects.get(admin=request.user.id)
        
        attendance=Attendance.objects.filter(attendance_date__range=(start_date_parse,end_date_parse),subject_id=subject_obj)
        attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
        

        attendance_report_data=[]
        for attendance_report in attendance_reports:
            data={"attendance_date":str(attendance_report.attendance_id.attendance_date),"status":attendance_report.status}
            attendance_report_data.append(data)
        
        return JsonResponse(json.dumps(attendance_report_data),safe=False)

    else:
        student=Students.objects.get(admin=request.user.id)
        course=student.course_id
        subjects=Subjects.objects.filter(course_id=course)
        return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})


def Student_Apply_Leave(request):
    student_obj=Students.objects.get(admin=request.user.id)
    if request.method == "POST":
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")
        try:
            leave_report=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg)
            leave_report.save()
            messages.success(request,"Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.success(request,"Failed to apply Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))

    else:
        leave_data=LeaveReportStudent.objects.filter(student_id=student_obj)
        return render(request,"student_template/student_apply_leave.html",{"leave_data":leave_data})

def Student_Feedback(request):
    student_obj=Students.objects.get(admin=request.user.id)
    if request.method == "POST":
        feedback_msg=request.POST.get("feedback_msg")
        try:
            feedback=FeedBackStudent(student_id=student_obj, feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request,"Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.success(request,"Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_data=FeedBackStudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_feedback.html",{"feedback_data": feedback_data})

def Student_Profile(request):
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

            student=Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse('student_profile'))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse('student_profile'))
    else:
        user=CustomUser.objects.get(id=request.user.id)
        student=Students.objects.get(admin=user)
        return render(request, 'student_template/student_profile.html',{"user":user,'student':student})


def Student_Result(request):
    student=Students.objects.get(admin=request.user.id)
    studentresult=StudentResult.objects.filter(student_id=student.id)
    return render(request,"student_template/student_result.html",{"studentresult":studentresult})