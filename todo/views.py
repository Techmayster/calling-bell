from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import User_information,Remote_information,data_logging
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import hashlib
from Send__email import send_OTP
import random
import pandas as pd
from datetime import date, timedelta
import datetime
from datetime import timedelta
from datetime import datetime 

admin_mail_id = "ajayladkat123@gmail.com"



def auth(request,user,pswd):
    try:
        user = authenticate(request, username=user, password=pswd)
        login(request, user)
        return redirect('dashboard')

    except:
        return render(request, 'todo/home.html',{'msg':'Unauthorized User'})


def TM_API(request,GWD_code,remote_code):
        get_received_remote_info_from_database = Remote_information.objects.all().filter(gateway_device_code = GWD_code).filter(remote_code = remote_code)

        if len(get_received_remote_info_from_database) == 0:
            
            msg = "Unknown remote information is received: \n\t\tGatewat Device Code : " + str(GWD_code) + " \n\t\t Remote code : " + str(remote_code)
            subject = "TechMayster: Remote updation need in admin panel with Gateway device code : " + str(GWD_code)
            send_OTP(subject,msg,admin_mail_id)
            insert_remote_info = Remote_information()
            insert_remote_info.gateway_device_code = GWD_code
            insert_remote_info.remote_code = remote_code
            insert_remote_info.save()

        else:
            if get_received_remote_info_from_database[0].verified == True:
                if get_received_remote_info_from_database[0].remote_type == "call":
                    info_of_received_remote = data_logging.objects.all().filter(Remote_Name = get_received_remote_info_from_database[0].remote_name).order_by('-Call_Time')
                    if len(info_of_received_remote) != 0:
                        if info_of_received_remote[0].Cancel_Time != None:
                            log_data = data_logging()
                            log_data.user_id = get_received_remote_info_from_database[0].user.id
                            log_data.Remote_Name = get_received_remote_info_from_database[0].remote_name
                            log_data.save()
                    else:
                        log_data = data_logging()
                        log_data.user_id = get_received_remote_info_from_database[0].user.id
                        log_data.Remote_Name = get_received_remote_info_from_database[0].remote_name
                        log_data.save()

                else:
                    info_of_received_remote = data_logging.objects.all().filter(Remote_Name = get_received_remote_info_from_database[0].remote_name).order_by('-Call_Time')
                    if len(info_of_received_remote) != 0:
                        if info_of_received_remote[0].Cancel_Time == None:
                            data_to_update = data_logging.objects.get(id = int(info_of_received_remote[0].id))
                            data_to_update.Cancel_Time = datetime.now()
                            data_to_update.save()

        return render(request, 'todo/home.html')



def home(request):
    return render(request, 'todo/home.html')


class convert_to_class:
    def __init__(self,a,b,c):
        self.data = a
        self.index = b
        self.color = c


@login_required
def dashboard(request):
    try:
        user_info = User_information.objects.all().filter(user_id = request.user.id)
        text_to_show_on_top = user_info[0].text_to_show_on_top
        num_of_rows = user_info[0].grid_size_row
        num_of_cols = user_info[0].grid_size_col
        colour_after_not_attending = user_info[0].colour_after_not_attending
        time_to_respond_in_min = user_info[0].time_to_respond_in_min
        status = user_info[0].status
        logged_data = data_logging.objects.all().filter(user_id = request.user.id).filter(Cancel_Time = None).order_by('Call_Time').values()
        if status == True:
            data_information = []   
            for i in range(num_of_rows * num_of_cols):        
                data_information.append(convert_to_class("","td","white"))
                if(i%num_of_cols == num_of_cols-1):
                    data_information.append(convert_to_class("","tr",""))

            i=-1
            if len(logged_data) != 0:
    
                for di in data_information:
                    i+=1
                    di.data = logged_data[i]["Remote_Name"]

                    current_time = datetime.now()
                    Call_Time = logged_data[i]['Call_Time'].replace(tzinfo=None) 
                    minutes = round(abs((current_time - Call_Time).total_seconds() / 60.0 - 330),2)
                    if minutes > time_to_respond_in_min:
                        di.color = colour_after_not_attending

                    if i >= len(logged_data)-1:
                        break
                

            return render(request, 'todo/dashboard.html',{"num_of_rows":num_of_rows,"num_of_cols":num_of_cols,"data_information":data_information,"text_to_show_on_top":text_to_show_on_top})
        else:
            return render(request, 'todo/dashboard.html',{"msg":"Inactive"})
    except:
        return render(request, 'todo/dashboard.html',{"msg":"User Information is not filled"})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'], password=request.POST['password1'],  last_name=request.POST['password1'] )
                user.save()
                msg = "New registraion is done with username : " + request.POST['username']
                subject = "New registration ( Username : " + request.POST['username'] + " )"
                send_OTP(subject,msg,admin_mail_id)
                return render(request, 'todo/home.html',{'msg':'Registration Done. '})
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            print(user)
            print(request)
            login(request, user)

            return redirect('dashboard')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


