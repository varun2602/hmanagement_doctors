from django.urls import path
from . import views 

urlpatterns = [
    path('create_data', views.create_data, name = 'create_data'),
    path('delete_data', views.delete_data, name = 'delete_data'),
    path('', views.index1, name = 'index1'),
    path('register_doctor', views.register_doctor, name = 'register_doctor'),
    path('logout_doc', views.logout_doc, name = 'logout_doc'),
    path('validate_email', views.validate_email, name = 'validate_email'),
    path('login_doc', views.login_doctor, name = 'login_doc'),
    path('create_appointment', views.create_appointment, name = 'create_appointment'),
    path('delete_appointment', views.delete_appointment, name = 'delete_appointment'),
    path('deactivate', views.deactivate_doctor, name = 'deactivate'),
    path('delete_doctor', views.delete_doctor, name = 'delete_doctor'),
    path('test_route', views.test_route, name = 'test_route'),
    path('get_doctor', views.get_doctor, name = 'get_doctor'),
    path('booked_appointments', views.booked_appointments, name = 'booked_appointments'),
    path('decline_appointment', views.decline_appointment, name = 'decline_appointment'),
    path('confirm', views.confirm, name = "confirm"),
    path('get_confirmed_appointments', views.get_confirmed_appointments, name = 'get_confirmed_appointments'),
    path('delete_confirmed_appointments', views.delete_confirmed_appointments, name = 'delete_confirmed_appoitnments'),
    path('get_confirmed_appointments_doc', views.get_confirmed_appointments_doc, name = 'get_confirmed_appointments_doc'),
    path('create_bill', views.create_bill, name = 'create_bill'),
    path('get_bill', views.get_bill,  name = 'get_bill')
]
