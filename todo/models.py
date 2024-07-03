from django.db import models
from django.contrib.auth.models import User
import string
import random
from datetime import datetime    


class User_information(models.Model):
    type_of_user = (('Hospital', 'Hospital'), ('Hotel', 'Hotel'), ('Restaurant', 'Restaurant'), ('OPD', 'OPD'), ('Office', 'Office'), ('Other', 'Other'))
    report_freq = (('No', 'No'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Half yearly', 'Half yearly'), ('Yearly', 'Yearly'))

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_information')
    status= models.BooleanField(default=False)
    name_of_site = models.CharField(max_length=40)
    user_type = models.CharField(max_length=40, choices=type_of_user)
    area_name = models.CharField(max_length=40)
    latitude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)
    time_to_respond_in_min = models.PositiveIntegerField()
    colour_after_not_attending = models.CharField(max_length=40)
    logo_image = models.ImageField(upload_to ='uploads/',null=True,blank=True) 
    text_to_show_on_top = models.CharField(max_length=100)
    grid_size_row = models.PositiveIntegerField()
    grid_size_col = models.PositiveIntegerField()
    frequency_of_report = models.CharField(max_length=40, choices=report_freq)
    Email_ID_for_report_1 = models.CharField(max_length = 150,blank=True)
    Email_ID_for_report_1 = models.CharField(max_length = 150,blank=True)
    gateway_device_code = models.CharField(max_length=40,null=True,blank=True)
    
    def __str__(self):
        if self.status == True:
            return self.name_of_site + " [ Area: " + self.area_name + " ] { User name: " + self.user.username + " }"
        else:
            return self.name_of_site + " [ Area: " + self.area_name + " ] { User name: " + self.user.username + " }    ---    < Inactive >"


class Remote_information(models.Model):
    r_type = (('call', 'call'), ('cancel', 'cancel') )

    gateway_device_code = models.CharField(max_length=40)
    remote_code = models.CharField(max_length=40)
    remote_name = models.CharField(max_length=40,null=True,blank=True)
    remote_type = models.CharField(max_length=40, choices=r_type,default='call')
    # user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='remote_information',null=True,blank=True)

    verified= models.BooleanField(default=False)
    def __str__(self):
        try:
            if self.verified == True:
                if self.remote_type == 'call':
                    return " [ user: " + self.user.username + " ] { GWD code: " + self.gateway_device_code + " } ( Remote name : " + self.remote_name + " ) [type : call]"
                else:
                    return " [ user: " + self.user.username + " ] { GWD code: " + self.gateway_device_code + " } ( Remote name : " + self.remote_name + " ) [type : cancel]"
            else:
                return "{GWD code: " + self.gateway_device_code + " } ( Remote name : " + self.remote_name + " )  ---  <Not verified>"
        except:
                return "{GWD code: " + self.gateway_device_code + " } ( Remote code : " + self.remote_code + " )  --- <User not assigned>"


class data_logging(models.Model):
    user_id = models.CharField(max_length=40)
    Remote_Name = models.CharField(max_length=40)
    Call_Time = models.DateTimeField(default=datetime.now, blank=True)    
    Cancel_Time = models.DateTimeField(null=True,blank=True)    

    def __str__(self):
        if self.Cancel_Time == None:
            return "[User ID: " + self.user_id + "] {Remote name: " + self.Remote_Name + "} : {Not attended yet]"
        else:
            return "[User ID: " + self.user_id + "] {Remote name: " + self.Remote_Name + "}"

