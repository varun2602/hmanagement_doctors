from django.contrib import admin
from manage_doctors import models


# Register your models here.


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['DoctorID', 'designation', 'email', 'work_hours_start', 'work_hours_end', 'doc_name']


@admin.register(models.BookAppointment)
class BookAdmin(admin.ModelAdmin):
    list_display = ['DoctorName', 'PatientName', 'DateOfAppointment']

@admin.register(models.ConfirmAppointment)
class ConfirmAdmin(admin.ModelAdmin):
    list_display = ['DoctorName', 'PatientName', 'DateOfAppointment']

@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['PatientName', 'insurance', 'fees', 'deduction', 'payable', 'date_of_bill']