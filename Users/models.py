from django.db import models
import time
import os
import uuid
from typing import Any


# def generate_unique_filename(instance: Any, filename: str):
#     _, ext = os.path.splitext(filename)

#     # Generate a unique filename using a combination of UUID, timestamp, and original filename
#     unique_filename = f"{uuid.uuid4()}_{int(time.time())}_{ext}"
    
#     return os.path.join('Users', str(instance.user_id), filename[:filename.index('.')] ,unique_filename)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)  # create primary key
    user_full_name = models.CharField(max_length=3,blank=False, null=False)
    user_password = models.CharField(max_length=100,blank=False, null=False)
    user_email = models.CharField(max_length=50,blank=False, null=False,unique=True) 
    user_phone = models.CharField(max_length=20,blank=False, null=False,unique=True)
    #profile_pic = models.ImageField(upload_to=generate_unique_filename,blank=True, null=True) # TODO: ADD
