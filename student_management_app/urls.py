from django.contrib import admin
from django.urls import path,include
from . import views
from . import Hodviews,Staffviews,Studentviews
urlpatterns = [
    path("",views.index, name="index"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('login',views.Login,name='login'),
    path('get_user_details',views.GetUserDetails,name='get_user_details'),
    path('logout_user',views.LogoutUser,name='logout_user'),
    
    path('admin_home',Hodviews.AdminHome,name='admin_home'),

    

    # path('admin_home_test', Hodviews.AdminHomeTest, name='admin_home'),  #testing
    

    path('add_staff',Hodviews.AddStaff,name='add_staff'),
    path('add_course',Hodviews.AddCourse,name='add_course'),
    path('add_student',Hodviews.AddStudent,name='add_student'),
    path('add_subject',Hodviews.AddSubject,name='add_subject'),

    path('manage_staff',Hodviews.ManageStaff,name='manage_staff'),
    path('manage_student',Hodviews.ManageStudent,name='manage_student'),
    path('manage_course',Hodviews.ManageCourse,name='manage_course'),
    path('manage_subject',Hodviews.ManageSubject,name='manage_subject'),

    path('edit_staff/<str:staff_id>',Hodviews.EditStaff,name='edit_staff'),
    path('edit_student/<str:student_id>',Hodviews.EditStudent,name='edit_student'),
    path('edit_subject/<str:subject_id>',Hodviews.EditSubject,name='edit_subject'),
    path('edit_course/<str:course_id>',Hodviews.EditCourse,name='edit_course'),
    path('manage_session_year',Hodviews.ManageSession_Year,name='manage_session'),
    path('staff_feedback_message',Hodviews.Staff_Feedback_Message,name='staff_feedback_message'),
    path('student_feedback_message',Hodviews.Student_Feedback_Message,name='student_feedback_message'),
    path('student_leave_report',Hodviews.Student_Leave,name='student_leave_report'),
    path('student_leave_action/<str:leave_id>/<str:action>',Hodviews.Student_Leave_Action,name='student_leave_action'),
    path('staff_leave_report',Hodviews.Staff_Leave,name='staff_leave_report'),
    path('staff_leave_action/<str:leave_id>/<str:action>',Hodviews.Staff_Leave_Action,name='staff_leave_action'),
     path('admin_view_attendance', Hodviews.Admin_View_Attendance,name="admin_view_attendance"),
   
    path('admin_get_attendance_dates',Hodviews.Admin_Get_Attendance_Dates,name='admin_get_attendance_dates'),
    path('admin_get_attendance_student',Hodviews.Admin_Get_Attendance_Student,name='admin_get_attendance_student'),
    path('admin_profile',Hodviews.Admin_Profile,name='admin_profile'),
    





    path('staff_home',Staffviews.StaffHome, name='staff_home'),
    path('staff_take_attendance',Staffviews.Staff_Take_Attendance, name='staff_take_attendance'),
    path('get_students',Staffviews.Get_Students, name='get_students'),
    path('save_attendance_data',Staffviews.Save_Attendance_Data, name='save_attendance_data'),
    path('staff_update_attendance',Staffviews.Staff_Update_Attendance, name='staff_update_attendance'),
    path('get_attendance_dates',Staffviews.Get_Attendance_dates, name='get_attendance_dates'),
    path('get_attendance_student',Staffviews.Get_Attendance_student, name='get_attendance_student'),
    path('update_attendance_data',Staffviews.Update_Attendance_Data, name='update_attendance_data'),
    path('staff_apply_leave',Staffviews.Staff_Apply_Leave, name='staff_apply_leave'),
    path('staff_feedback',Staffviews.Staff_Feedback, name='staff_feedback'),
    path('staff_profile',Staffviews.Staff_Profile,name='staff_profile'),
    path('staff_add_result',Staffviews.Staff_Add_Result,name='staff_add_result'),
    path('staff_edit_result',Staffviews.Staff_Edit_Result,name='staff_edit_result'),
    path('fetch_result_student',Staffviews.Fetch_Result_Student,name='fetch_result_student'),
    
    


    path('student_home',Studentviews.StudentHome, name='student_home'),
    path('student_view_attendance',Studentviews.Student_View_Attendance, name='student_view_attendance'),
    path('student_apply_leave',Studentviews.Student_Apply_Leave, name='student_apply_leave'),
    path('student_feedback',Studentviews.Student_Feedback, name='student_feedback'),
    path('student_profile',Studentviews.Student_Profile,name='student_profile'),
    path('student_result',Studentviews.Student_Result,name='student_result'),
    




]
