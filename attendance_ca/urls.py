"""attendance_ca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from employee_attendance import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', views.home),
    url(r'^admin/upload_details/', views.upload_resume, name='upload'),
    # url(r'^jet/', include('jet.urls', 'jet')),
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^employee/', include('employee_attendance.urls')),
    url(r'^admin/employee_attendance/(?P<pk>[0-9]+)/approve_leave/', views.approve_leave),
    url(r'^admin/employee_attendance/(?P<pk>[0-9]+)/reject_leave/', views.reject_leave),
    url(r'^admin/employee_attendance/(?P<pk>[0-9]+)/availed_reimbursement/', views.availed_reimbursement),
    url(r'^admin/employee_attendance/(?P<pk>[0-9]+)/approve_reimbursement/', views.approve_reimbursement),
    url('', views.log_in_employee),
]
