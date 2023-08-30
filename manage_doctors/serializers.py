from rest_framework import serializers 
import uuid
from . import models

class PatientSerializer(serializers.Serializer):
    username  = serializers.CharField(max_length  = 100, allow_null = True, allow_blank = True)
    company_name = serializers.CharField(max_length = 100, allow_blank = True, allow_null = True)
    company_designation = serializers.CharField(max_length = 100, allow_blank = True, allow_null = True)
    insurance = serializers.CharField(max_length = 50, allow_null = True, allow_blank = True)

    def create(self, validated_data):
        return models.Patients.objects.create(**validated_data)
    
class DoctorSerializer(serializers.Serializer):
    DoctorID = serializers.CharField(max_length = 10, default = uuid.uuid4)
    designation = serializers.CharField(max_length = 100, allow_blank = True, allow_null = True)
    doc_name = serializers.CharField(max_length = 100, allow_blank = True, allow_null = True)
    email = serializers.EmailField(max_length = 100, allow_null = True, allow_blank = True)

class BookAppointmentSerializer(serializers.Serializer):
    DoctorName = serializers.CharField(max_length = 100, allow_null = True, allow_blank= True)
    PatientName = serializers.CharField(max_length = 100, allow_null = True, allow_blank = True)
    DateOfAppointment = serializers.DateTimeField(allow_null = True) 

    def create(self, validated_data):
        return models.BookAppointment.objects.create(**validated_data)
    
class ConfirmSerializer(serializers.Serializer):
    DoctorName = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    PatientName = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    DateOfAppointment = serializers.CharField(allow_null=True, allow_blank= True)

class BillSerializer(serializers.Serializer):
    PatientName = serializers.CharField(max_length = 100, allow_null = True, allow_blank = True)
    insurance =serializers.CharField(max_length= 100, allow_null = True, allow_blank = True)
    fees = serializers.IntegerField(default = 100)
    deduction = serializers.IntegerField(default = 0)
    date_of_bill = serializers.DateTimeField(allow_null = True, required = False)
    payable = serializers.IntegerField(default = 100)

    def create(self, validated_data):
        return models.Bill.objects.create(**validated_data)