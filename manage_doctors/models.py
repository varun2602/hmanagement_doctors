from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import uuid


# Create your models here.
class Patients(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True, unique = True)
    email = models.CharField(max_length = 100, blank = True, null = True, unique = True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_designation = models.CharField(max_length=100, blank=True, null=True)
    insurance = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"PatientAPI: {self.username}"


class Doctor(AbstractUser):
    DoctorID = models.CharField(max_length=10, primary_key=True, default=uuid.uuid4, editable=False)
    doc_name = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    work_hours_start = models.TimeField(default=datetime.time(9, 0))
    work_hours_end = models.TimeField(default=datetime.time(17, 0))

    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions', blank=True
    )
    USERNAME_FIELD = 'email'

    

    def __str__(self):
        return f"Doctor: {self.email}"


class BookAppointment(models.Model):
    DoctorName = models.CharField(max_length=100, null=True, blank=True)
    PatientName = models.CharField(max_length=100, null=True, blank=True)
    DateOfAppointment = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booked: {self.DoctorName} and {self.PatientName}"
    
class ConfirmAppointment(models.Model):
    DoctorName = models.CharField(max_length=100, null=True, blank=True)
    PatientName = models.CharField(max_length=100, null=True, blank=True)
    DateOfAppointment = models.CharField( max_length = 100, null=True, blank=True)

    def __str__(self):
        return f"Confirmed: {self.DoctorName} and {self.PatientName}"
    
class Bill(models.Model):
    PatientName = models.CharField(max_length = 100, null = True, blank = True)
    insurance = models.CharField(max_length= 100, null = True, blank = True)
    fees = models.IntegerField(default = 100)
    deduction = models.IntegerField(default = 0)
    date_of_bill = models.DateTimeField(auto_now_add= True)
    payable = models.IntegerField(default = 100)

    def __str__(self):
        return f'Bill: {self.payable}'

