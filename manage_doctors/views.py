from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from . import models
from . import serializers
import json
import io

# from . import jwt_adapter

current_login_name = []
# Create your views here.
@login_required(login_url="/manage_doctors/login_doc")
def index1(request):
    print('Index1')
    # if not jwt_adapter.is_logged_in(request):
    #     print('Not logged in')
        # return HttpResponseRedirect(reverse('login_doc'))
    return render(request, 'index1.html')

# Doctor Registration 
@csrf_exempt
def register_doctor(request):
    if request.method == 'GET':
        return render(request, 'register_doctor.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        doc_name = request.POST.get('doc_name')
        doc_designation = request.POST.get('doc_designation')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Check if passwords match
        if password != cpassword:
            data = {'message':'Passwords do not match'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
        
        # Check if user exists, if not register
        try:
            user_exists = models.Doctor.objects.get(email = email)
            data = {'message':'User already exists'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
        except models.Doctor.DoesNotExist:
            user_create = models.Doctor.objects.create(doc_name = doc_name, email = email, designation = doc_designation, password = password)
            user_create.save()
            data = {'message':'Registered successfully!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
        
# Validate input email on registration form
@csrf_exempt 
def validate_email(request):
    email = request.POST.get('email_input')
    try:
        email_exists = models.Doctor.objects.get(email = email)
        data = {'r':200}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = 'application/json')
    except models.Doctor.DoesNotExist:
        data = {'r':20}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = 'application/json')


@csrf_exempt
def login_doctor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists  
        try:
            user = models.Doctor.objects.get(email = email)
            user_exists = authenticate(request, username = email, password = password)
            if user_exists is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("/"))
            else:
                context = {"message": "Invalid username or password!"}
                return render(request, "login_doc.html", context)
        except models.Doctor.DoesNotExist:
            context = {"message": "User does not exist"} 
            return render(request, "login_doc.html", context)

    else:
        return render(request, "login_doc.html")

            

        
    

# Logout 
def logout_doc(request):
    logout(request)
    current_login_name = []
    return HttpResponseRedirect(reverse('index'))
    

# PATIENT CRUD 
@csrf_exempt
def create_data(request):
    if request.method == 'POST':
        json_data = request.body 
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serialized = serializers.PatientSerializer(data = python_data)
        if serialized.is_valid():
            serialized.save()
            data = {'message':'Data created successfully!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serialized.errors)
        return HttpResponse(json_data, content_type = 'application/json')

@csrf_exempt
def delete_data(request):
    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        username = python_data.get('username', None)
        if username is not None:
            try:
                patient = models.Patients.objects.get(username = username)
                patient.delete()
                data = {'message':'Deleted successfully'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type = 'application/json')
            except models.Patients.DoesNotExist:
                data = {'message':'Username does not exist'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type = 'application/json')
        data = {'message':'Invalid request'}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = 'application/json')
# DOCTOR CRUD 
@csrf_exempt
def get_doctor(request):
    json_data = request.body
    # print("JSON", json_data)
    stream = io.BytesIO(json_data)
    # print("Stream",stream)
    python_data = JSONParser().parse(stream)
    name = python_data.get('name', None)
    # print(name)
    if name is not None:
        try:
            doctor = models.Doctor.objects.get(doc_name = name)
            serialized = serializers.DoctorSerializer(doctor)
            json_data = JSONRenderer().render(serialized.data)
            return HttpResponse(json_data, content_type = 'application/json')
        except models.Doctor.DoesNotExist:
            data = {'message':'Doctor does not exists!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
    else:
        all_doctors = models.Doctor.objects.all()
        serialized = serializers.DoctorSerializer(all_doctors, many = True)
        json_data = JSONRenderer().render(serialized.data)
        return HttpResponse(json_data, content_type = 'application/json')
    
@csrf_exempt
def delete_doctor(request):
    if request.method == 'DELETE':
        json_data = request.body 
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        name = python_data.get('name', None)
        if name is not None:
            try:
                doctor_name = models.Doctor.objects.get(doctor_name = name)
                doctor_name.delete()
                data = {'message':'Doctor record deleted successfully'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type = 'application/json')
            except models.Doctor.DoesNotExist:
                data = {'message':'Doctor does not exists!'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type= 'application/json')
        else:
            all_doctors = models.Doctor.objects.all()
            all_doctors.delete()
            data = {'message':'All records deleted successfully!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data)
            


@csrf_exempt
def deactivate_doctor(request):
    doctor_to_deactivate = request.user.username
    logout(request)
    doctor_model = models.Doctor.objects.get(doctor_to_deactivate)
    return HttpResponseRedirect(reverse('index'))



# Appointment CRUD
@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serialized = serializers.BookAppointmentSerializer(data = python_data)
        if serialized.is_valid():
            serialized.save()
            data = {'message':"Appointment booked successfully"}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serialized.errors)
        return HttpResponse(json_data, content_type = 'application/json')
@csrf_exempt
def delete_appointment(request):
    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        doc_name = python_data.get('doc_name', None)
        patient_name = python_data.get('patient_name', None)
        
        if doc_name is not None and patient_name is not None:
            try:
                appointment = models.BookAppointment.objects.get(DoctorName = doc_name, PatientName = patient_name)
                appointment.delete()
                data = {'message':'Appointment cancelled successfully'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type = 'application/json')
            except models.BookAppointment.DoesNotExist:
                data = {'message':'Appointment does not exists!'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type = 'applicatioon/json')
        else:
            all_appointments = models.BookAppointment.objects.all()
            all_appointments.delete()
            data = {'message':'All entries deleted!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
@csrf_exempt
def booked_appointments(request):
    if request.method == 'GET':
        doc_email = current_login_name[0]
        doctor = models.Doctor.objects.get(email = doc_email)
        # return HttpResponse(f'{doc_email} {doctor.email} {doctor.doc_name}')
        appointments = models.BookAppointment.objects.filter(DoctorName = doctor.doc_name)
        context = {'appointments':appointments}
        return render(request, 'booked_appointments.html', context)
    
# Confirmed Appointment API CRUD 
@csrf_exempt
def get_confirmed_appointments(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        patient_name = python_data.get('patient_name', None)
        print("Patient:",patient_name)
        if patient_name is not None:
            confirmed = models.ConfirmAppointment.objects.filter(PatientName = patient_name)
            if not confirmed:
                data = {'message':'You have no confirmed appointments'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type = 'application/json')
            serialized = serializers.ConfirmSerializer(confirmed, many = True)
            json_data = JSONRenderer().render(serialized.data)
            return HttpResponse(json_data, content_type = 'application/json')
        else:
            all_appointments = models.ConfirmAppointment.objects.all()
            serialized = serializers.ConfirmSerializer(all_appointments, many = True)
            json_data = JSONRenderer().render(serialized.data)
            return HttpResponse(json_data, content_type = 'application/json')
        
@csrf_exempt
def delete_confirmed_appointments(request):
    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        patient_name = python_data.get('patient_name', None)
        if patient_name is not None:
            confirmed = models.ConfirmAppointment.objects.filter(PatientName = patient_name)
            confirmed.delete()
            data = {'message':'Data deleted successfully'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
        all_confirmed = models.ConfirmAppointment.objects.all()
        all_confirmed.delete()
        data = {'message':'All confirmed appointments deleted'}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = 'application/json')

    
            
            
        


@csrf_exempt
def test_route(request):
    return render(request, 'test1.html')

@csrf_exempt
def confirm(request):
    doctor_name = request.POST.get('doctor')
    patient_name = request.POST.get('patient')
    date_time = request.POST.get('datetime')

    # Generate Bill 
    patient_obj = models.Patients.objects.get(username = patient_name)
    insurance = patient_obj.insurance 
    if insurance == 'None':
        fees = 100
        deduction = 0
        payable = fees - deduction 
    elif insurance == 'Partial':
        fees = 100
        deduction = 0.8*fees
        payable = fees - deduction
    elif insurance == 'Complete':
        fees = 100
        deduction = fees 
        payable = fees - deduction 
    Bill = models.Bill.objects.create(PatientName = patient_name, insurance = insurance, deduction = deduction, payable = payable)
    Bill.save()



    # print(doctor_name, patient_name, date_time)
    confirmed = models.ConfirmAppointment.objects.create(DoctorName = doctor_name, PatientName = patient_name, DateOfAppointment = date_time)
    confirmed.save()
    delete_booked = models.BookAppointment.objects.filter(DoctorName = doctor_name, PatientName = patient_name)
    delete_booked.delete()
    data = {'message':'Confirmed successfully!'}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type = 'application/json')

@csrf_exempt
def decline_appointment(request):
    doctor_name = request.POST.get('doctor')
    patient_name = request.POST.get('patient')
    
    # date_time = request.POST.get('date_time')
    
    # date_obj = datetime.strptime(date_str, "%b %d, %Y, %I:%M %p")

    to_delete = models.BookAppointment.objects.filter(DoctorName = doctor_name, PatientName = patient_name)
    to_delete.delete()

    data = {'message':'Declined successfully'}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type = 'application/json')

def get_confirmed_appointments_doc(request):
    if request.method == 'GET':
        doctor_email = current_login_name[0]
        doctor = models.Doctor.objects.get(email = doctor_email)
        doctor_name = doctor.doc_name
    
        all_confirmed = models.ConfirmAppointment.objects.filter(DoctorName = doctor_name)
    
        context = {'all_confirmed':all_confirmed}
        return render(request, 'confirmed.html', context)
# Bill CRUD 
@csrf_exempt
def create_bill(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serialized = serializers.BillSerializer(data = python_data)
        if serialized.is_valid():
            serialized.save()
            data = {'message':'Bill created successfully'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serialized.errors)
        return HttpResponse(json_data, content_type = 'application/json')
def get_bill(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        patient_name = python_data.get('patient_name', None)
        print(patient_name)
        if patient_name is not None:
            Bill = models.Bill.objects.filter(PatientName = patient_name)
            serialized = serializers.BillSerializer(Bill, many = True)
            json_data = JSONRenderer().render(serialized.data)
            return HttpResponse(json_data, content_type = 'application/json')
        all_bills = models.Bill.objects.all()
        serialized = serializers.BillSerializer(all_bills, many = True)
        json_data = JSONRenderer().render(serialized.data)
        return HttpResponse(json_data, content_type = 'application/json')
    





"""
@csrf_exempt
def login_doctor(request):
    if request.method == 'GET':
        return render(request, 'login_doc.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check if user exists 
        try:
            user_exists = models.Doctor.objects.get(username = email)

            # - PROBLEM LIES THERE
            user_create = authenticate(username = email, password = password)
            print(user_create)

            if user_create is not None:
                login(request, user_create)
                return HttpResponseRedirect(reverse('index1'))
            else:
                context = {'message':'Invalid credentials'}
                return render(request, 'login_doc.html', context)
            # END PROBLEM
        except models.Doctor.DoesNotExist:
            context = {'message':'User does not exists!'}
            return render(request, 'login_doc.html', context)
"""
        

