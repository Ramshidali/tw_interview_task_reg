from django.db import models
from django.contrib.auth.models import User

from main.models import BaseModel
from main.variables import phone_regex

# Create your models here.
USER_ROLES =(
    ("admin_user", "Admin"),
    ("staff", "Staff"),
    ("editor", "Editor"),
    ("student", "Student"),
)

class UserDetails(BaseModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    role = models.CharField(choices=USER_ROLES,max_length=10)
    country = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10 , validators=[phone_regex], unique=True)
    password = models.CharField(max_length=256,null=True,blank=True)
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
        
    class Meta:
        db_table = 'user_details'
        verbose_name = ('User Details')
        verbose_name_plural = ('User Details')
    
    def __str__(self):
        return str(self.name)