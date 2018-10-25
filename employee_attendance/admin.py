from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html

from .models import Employee, Log, Attendance, Leave, Holiday, ReimbursementType, Reimbursement
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from . import views

# Register your models here.

admin.site.site_header = 'Cloud Analogy'
admin.site.index_title = 'CA Attendance Portal'
admin.site.site_title = 'CA administration'


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['__str__', 'employee_id']
    # list_display = [f.name for f in Employee._meta.get_fields()]
    # ignore_fields = ['attendance', 'log', 'leave', 'reimbursement']


class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance

    list_filter = ['employee']

    def in_time(self, obj):
        return obj.ca_emp_in_time.time()

    def out_time(self, obj):
        if obj.ca_emp_out_time:
            return obj.ca_emp_out_time.time()
        return obj.ca_emp_out_time

    list_display = ['id', 'employee', 'date', 'in_time', 'out_time']


class HolidayAdmin(admin.ModelAdmin):
    model = Holiday
    list_display = [f.name for f in Holiday._meta.get_fields()]


class LeaveAdmin(admin.ModelAdmin):
    model = Leave
    list_display = ['employee_id']
    list_display.extend([f.name for f in Leave._meta.get_fields()
                         if f.name not in ('from_session','to_session',
                                           'grant_expire_date','id')])
    list_display.extend(['approve_leave',
                         'reject_leave'])
    actions = ['approve_leaves',
               'reject_leaves']
    list_filter = ['status',
                   'employee_id']

    def approve_leaves(self, request, queryset):
        for object in queryset:
            views.approve_leave(request, object.id)

    def get_actions(self, request):
        actions = super(LeaveAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def employee_id(self, obj = None):
        if obj:
            return obj.employee.employee_id

    def reject_leaves(self, request, queryset):
        for object in queryset:
            views.reject_leave(request, object.id)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in Leave._meta.get_fields() if f.name not in ('status')]
        return []

    def approve_leave(self, obj):
        return format_html('<a class="btn btn-success" '
                           +'href="/admin/employee_attendance/{pk}/approve_leave/">Approve</a>',
                           pk=obj.pk)

    def reject_leave(self, obj):
        return format_html('<a class="btn btn-success" '
                           +'href="/admin/employee_attendance/{pk}/reject_leave/">Reject</a>',
                           pk=obj.pk)


class ReimbursementAdmin(admin.ModelAdmin):
    model = Reimbursement
    list_display = [f.name for f in Reimbursement._meta.get_fields()]
    list_display.extend(['approve_reimbursement', 'reject_reimbursement'])
    list_display.remove('bill')

    def approve_reimbursement(self, obj):
        if obj.status == 'Pending':
            return format_html('<a class="btn btn-success" '
                               +'href="/admin/employee_attendance/{pk}/approve_reimbursement/">Approve</a>',
                               pk=obj.pk)
        return format_html( 'response done' )

    def reject_reimbursement(self, obj):

        if obj.status != 'Availed':
            return format_html( '<a class="btn btn-success" '
                                + 'href="/admin/employee_attendance/{pk}/availed_reimbursement/">Diposited in account</a>',
                                pk=obj.pk )
        return format_html( 'response done' )



# admin.site.register(Cloudanalogy_User_c)
# admin.site.unregister(Group)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(ReimbursementType)
admin.site.register(Reimbursement, ReimbursementAdmin)
# admin.site.register(Log, LogAdmin)
admin.site.register(Leave,LeaveAdmin)
admin.site.register(Holiday, HolidayAdmin)
