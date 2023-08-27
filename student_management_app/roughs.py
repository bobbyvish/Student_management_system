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
