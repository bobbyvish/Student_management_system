from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from student_management_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout
from django.urls import reverse


def Login(request):
    if request.method == 'POST':
        username=request.POST.get('email')
        password=request.POST.get('password')
        user=EmailBackEnd.authenticate(request,username=username,password=password)
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse('staff_home'))
            else:
                return HttpResponseRedirect(reverse('student_home'))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'login.html')

def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User :"+request.user.email+" usertype :"+request.user.user_type)
    else:
        return HttpResponse("Please login first")

def LogoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))