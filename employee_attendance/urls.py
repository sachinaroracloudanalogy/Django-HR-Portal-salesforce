
from django.conf.urls import include, url
# from django.urls import path

from . import views

app_name = 'employee_attendance'

urlpatterns = [
    url( r'^$', views.log_in_employee ),
    url( r'^login/', views.log_in_employee, name='login'),
    url(r'^logout/', views.log_out_employee, name='logout'),
    url(r'^attend_in/', views.attend_in, name='attend_in'),
    url(r'^attend_out/', views.attend_out, name='attend_out'),
    url(r'^attendance_details/', views.attendance_details, name='attendance_details'),
    url(r'^leave_details/', views.leave_details, name='leave_details'),
    url(r'^apply_leaves/', views.apply_leaves, name='apply_leaves'),
    url(r'^apply_reimbursement/', views.apply_reimbursement, name='apply_reimbursement'),
    url(r'^holiday_details/', views.holiday_details, name='holiday_details'),
    url(r'^reimbursement_details/', views.reimbursement_details, name='reimbursement_details' )
    ]