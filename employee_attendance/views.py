"""
    dfegrth
"""
from datetime import datetime, date, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from employee_attendance.utils.sf_api import SFConnectAPI
from .forms import LeaveForm, DateRangeForm, LogInForm, ReimbursementForm
from .models import Attendance, Holiday, Log, Employee, Leave, Reimbursement
from .tables import LeavesTable, AttendanceTable, HolidayTable, ReimbursementTable
from collections import OrderedDict

sf_instance = SFConnectAPI()
Employee_main = {}


def home(request):
    return render(request,
                  "form.html",
                  {'designations': ['Developer', 'Consultant', 'HR', 'QA', 'Bussiness Developer Executive', 'Content Writer', 'UI Developer', 'Sales Executive', 'Web Developer', 'Sales']},)


def log_in_employee(request):
    """
    :param request:
    :return:
    """
    request.session.set_expiry(300)

    if 'ca_user' in request.session and request.session['ca_user'] != '':
        print('Login method')
        # emp = Employee.objects.get(username=request.session['ca_user'])

        try:
            # ca_attendance = Attendance.objects.filter(employee=emp).order_by('-id')[0]
            emp = sf_instance.execute_soql( "select id,Name,username__c,address__c,designation__c,dob__c,Employee_Id__c" \
                                            " from Employee__c where username__c='{username}'" \
                                            .format( username=request.session['ca_user'],))

            Employee_main.update(emp["records"][0])
            attendance_record = sf_instance.execute_soql( "select id,Name,out_time__c,in_time__c from Attendance__c" \
                                                          " where date__c={date} AND employee__c='{emp}'" \
                                                          .format( date=date.today(),
                                                                   emp=request.session['user_id']))
        except:
            attendance_record = False
        if attendance_record and attendance_record['totalSize'] and not attendance_record['records'][0]['in_time__c']:
            attend = True
        else:
            attend = False
        return render(request, 'user_details.html',
                      {'status': 'Login',
                       'item': Employee_main,
                       'attend': attend})

    elif request.method == 'POST':
        form = LogInForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        emp = sf_instance.execute_soql( "select id,Name,username__c,address__c,designation__c,dob__c,Employee_Id__c" \
                                        " from Employee__c where username__c='{username}' " \
                                        "AND password__c ='{password}'".format(username=username,
                                                                               password=password))
        if emp["records"]:
            Employee_main.update(emp["records"][0])
            # emp = list(Employee.objects.filter(username=username,
            #                                    password=password))
            employee_record = emp['records'][0]
        if emp['totalSize'] > 0:
            request.session['ca_user'] = username
            request.session['user_id'] = employee_record['Id']

            # out_time__c})
            # log_obj = Log(employee=emp[0])
            # log_obj.in_time = datetime.now()
            # log_obj.save()
            # print('in_time: ' + repr(log_obj.in_time))
            # ca_attendance = list(Attendance.objects.filter(employee=emp[0]).order_by('-id'))
            attendance_record = sf_instance.execute_soql( "select id,Name,out_time__c,in_time__c from Attendance__c" \
                                                          " where date__c={date} AND employee__c='{emp}'" \
                                                          .format(date=date.today(),
                                                                  emp=request.session['user_id'] ) )

            if attendance_record and attendance_record['totalSize'] and attendance_record['records'][0]['in_time__c']:
                attend = True
                if attendance_record['records'][0]['out_time__c']:
                    attend = False
            else:
                attend = False

            return render(request, 'user_details.html',
                          {'status': 'Login',
                           'item': Employee_main,
                           'attend': attend})

        messages.error(request,
                       ' Invalid username and password ')
        return HttpResponseRedirect('/')
    form = LogInForm()
    return render(request,
                  'log_in.html',
                  {'status': 'Logout', 'form': form})


def log_out_employee(request):
    """
    :param request:
    :return:
    """
    # if 'ca_user' in request.session and request.session['ca_user'] != '':
        # emp = Employee.objects.get(username=request.session['ca_user'])
        # log = Log.objects.filter(employee=emp).order_by('-id')[0]
        # log.out_time = datetime.now()
        # log.save()
        # print('out_time: ' + repr(log.out_time))
    request.session['ca_user'] = ''
    Employee_main = {}
    return HttpResponseRedirect('/')


def attend_in(request):
    """
    :param request:
    :return:
    """
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        # emp = Employee.objects.get(username=request.session['ca_user'])
        # ca_attendance = Attendance(employee=emp)
        # ca_attendance.ca_emp_in_time = datetime.now()
        #
        # ca_attendance.save()

        attendance_record = sf_instance.execute_soql( "select id,Name,out_time__c,in_time__c from Attendance__c" \
                                                      " where date__c={date} AND employee__c='{emp}'" \
                                                      .format( date=date.today(),
                                                               emp=request.session['user_id'] ) )
        if attendance_record['totalSize']:
            messages.error(request, 'Already Attendance taken !!!')
        else:
            result = sf_instance.create_record(object_name='Attendance__c',
                                               data={'date__c': str(date.today()),
                                                     'Employee__c': request.session['user_id'],
                                                     'in_time__c': str(datetime.now().time()),
                                                    })
            if result['success']:
                attend =True
                messages.info(request, 'PUNCH IN SUCCESSFULLY !!!' )
            else:
                attend = False
            return render(request, 'user_details.html',
                          {'status': 'Login',
                           'item': Employee_main,
                           'attend': attend})
    return HttpResponseRedirect('/')


def attend_out(request):
    """
    :param request:
    :return:
    """
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        # emp = Employee.objects.get(username=request.session['ca_user'])
        # ca_attendance = Attendance.objects.filter(employee=emp).order_by('-id')[0]
        # if ca_attendance.date == datetime.today().date():
        #     ca_attendance.ca_emp_out_time = datetime.now()
        # else:
        #     ca_attendance.ca_emp_out_time = ca_attendance.ca_emp_in_time + timedelta(hours=5)
        #
        # ca_attendance.save()
        attendance_record = sf_instance.execute_soql( "select id,Name,out_time__c,in_time__c from Attendance__c" \
                                                      " where date__c={date} AND employee__c='{emp}'" \
                                                      .format( date=date.today(),
                                                               emp=request.session['user_id'] ) )
        sf_instance.update_record(object_name='Attendance__c',
                                  record_id=attendance_record['records'][0]['Id'],
                                  data={'out_time__c':str(datetime.now().time())})
        messages.success( request, 'PUNCH OUT SUCCESSFULLY !!!' )
        return render( request, 'user_details.html',
                       {'status': 'Login',
                        'item': Employee_main,
                        'attend': False})
    return HttpResponseRedirect('/')


def attendance_details(request):
    """
    :param request:
    :return:
    """
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        if request.method == 'POST':
            form = DateRangeForm(request.POST)
            if form.is_valid():
                date_range_with_format = list(form.cleaned_data['date_range_with_format'])
                # emp = Employee.objects.get(username=request.session['ca_user'])
                # date_range_with_format[1] += timedelta(days=1)
                # print('dates: : : : : : : : : : ', str(date_range_with_format[0]))
                # attendances = Attendance.objects.filter(employee=request.session['user_id'],
                #                                         ca_emp_in_time__range=date_range_with_format).order_by(
                #                                                               '-ca_emp_in_time')

                attendances = sf_instance.execute_soql("select id,Name,date__c,out_time__c,in_time__c from Attendance__c where date__c >={start_date} " \
                                                       "AND date__c <={end_date}".format(start_date=date_range_with_format[0],
                                                                                         end_date=date_range_with_format[1]))

                if not attendances['totalSize']:
                    messages.error(request, 'No record found Select another date !!! ')
                else:
                    table = AttendanceTable(attendances['records'])
                    return render(request, 'attendance_details.html',
                                  {'status': 'Login', 'form': form,
                                   'table': table, 'date': True, })
                return render(request, 'attendance_details.html',
                              {'status': 'Login',
                               'form': form,
                               'attendance': attendances,
                               'date': True, })

        form = DateRangeForm()
        attendances = sf_instance.execute_soql(
            "select id,Name,date__c,out_time__c,in_time__c from Attendance__c limit 10")
        # {k, datetime.time(v)} if k =='out_time__c' or k=='in_time__c' else {k,v} for k, v in record
        records = list(attendances['records'])
        # for record in records:
        #     final_records = [{k, datetime.strptime(v,'%H:%M:%S.%fZ').time()} if k =='out_time__c' or k=='in_time__c' else {k:v} for k,v in record.items()]
        table = AttendanceTable(records)
        return render(request, 'attendance_details.html',
                      {'status': 'Login',
                       'attendance': False,
                       'table': table,
                       'date': False,
                       'form': form, })
    return HttpResponseRedirect('/')


def apply_leaves(request):
    """
    :param request:
    :return:
    """
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        print('applyleave method')
        print(str(request.method))
        if request.method == 'POST':
            print('in_post_method')
            form = LeaveForm(request.POST)
            print('form : : : : ' + str(form))
            if form.is_valid():
                leave_dates = list(form.cleaned_data['leave_dates'])
                employee = Employee.objects.get(username=request.session['ca_user'])
                leave = Leave(
                    employee=employee,
                    type_of_leave=form.cleaned_data['type_of_leave'],
                    type_of_transaction=form.cleaned_data['type_of_transaction'],
                    #reason_for_leave=form.cleaned_data['reason_for_leave'],
                    remarks=form.cleaned_data['remarks'],
                    leave_from=leave_dates[0],
                    leave_to=leave_dates[1],
                    leave_days=abs((leave_dates[1] - leave_dates[0]).days) + 1)
                # leaves = Leave.objects.filter(employee=employee)
                leave.save()
                return HttpResponseRedirect('/employee/leave_details/')
        form = LeaveForm()
        return render(request, 'leave_page.html',
                      {'status': 'Login',
                       'form': form})
    return HttpResponseRedirect('/')


def leave_details(request):
    """
    :param request:
    :return:
    """
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        print('leave_details')
        employee = Employee.objects.get(username=request.session['ca_user'])
        table = LeavesTable(Leave.objects.filter(employee=employee))
        table_title = 'Leaves Details'
        return render(request, 'leave_details.html',
                      {'status': 'Login',
                       'table': table,
                       'table_title': table_title})
    return HttpResponseRedirect('/')


def holiday_details(request):
    """
    :param request:
    :return:
    """
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        table = HolidayTable(Holiday.objects.all().order_by('date'))
        table_title = 'Holidays details'
        return render(request, 'leave_details.html',
                      {'status': 'Login',
                       'table': table,
                       'table_title': table_title})
    return HttpResponseRedirect('/')


def approve_leave(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    if request.user:
        leave = Leave.objects.get(pk=pk)
        leave.status = 'approved'
        leave.save()
        return HttpResponseRedirect('/admin/employee_attendance/leave/')
    return HttpResponseRedirect('/')


def reject_leave(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    if request.user:
        leave = Leave.objects.get(pk=pk)
        leave.status = 'rejected'
        leave.save()
        return HttpResponseRedirect('/admin/employee_attendance/leave/')
    return HttpResponseRedirect('/')


def apply_reimbursement(request):
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        print(str(request.method))
        if request.method == 'POST':
            print('in_post_method')
            form = ReimbursementForm(request.POST)
            print('form : : : : ' + str(form))
            if form.is_valid():
                employee = Employee.objects.get(username=request.session['ca_user'])
                reimbursement = Reimbursement(employee=employee,
                                              billing_date=form.cleaned_data['billing_date'],
                                              type=form.cleaned_data['type'],
                                              amount=form.cleaned_data['amount'],
                                              description=form.cleaned_data['description'],
                                              status='Pending',
                                              applied_date=datetime.today().date())
                reimbursement.save()
                return HttpResponseRedirect('/employee/reimbursement_details/')
        form = ReimbursementForm()
        # request.POST["billing_date"]
        return render(request, 'reimbursement_page.html',
                      {'status': 'Login',
                       'form': form})
    return HttpResponseRedirect('/')


def calculate_rebursement_employee(request, rebursement_id):
    # TODO: write code to calculate rebursement per employee
    pass


def calculate_overall_reimbursement(request):
    # TODO: write code to calculate total rebursement in a date range
    pass


def reimbursement_details(request):
    if 'ca_user' in request.session and request.session['ca_user'] != '':
        emp = Employee.objects.get( username=request.session['ca_user'] )
        if request.method == 'POST':
            form = DateRangeForm(request.POST)
            if form.is_valid():
                date_range_with_format = list(form.cleaned_data['date_range_with_format'])
                date_range_with_format[1] += timedelta(days=1)
                print('dates: : : : : : : : : : ', str(date_range_with_format[0]))
                reinmbursements = Reimbursement.objects.filter(employee=emp,
                                                               applied_date__range=
                                                               date_range_with_format).order_by(
                                                               '-applied_date')

                if not reinmbursements:
                    messages.error(request, 'No record found Select another date !!! ')
                else:
                    table = ReimbursementTable(reinmbursements)
                    return render(request, 'reimbursement_details.html',
                                  {'status': 'Login',
                                   'form': form,
                                   'table': table,
                                   'date': True, })
                return render(request, 'reimbursement_details.html',
                              {'status': 'Login',
                               'form': form,
                               'attendance': reinmbursements,
                               'date': True, })
        form = DateRangeForm()
        reinmbursements = Reimbursement.objects.filter(employee=emp).order_by(
            '-applied_date' )[:10]
        table = ReimbursementTable( reinmbursements )
        return render(request, 'reimbursement_details.html',
                      {'status': 'Login',
                       'attendance': False,
                       'date': False,
                       'table': table,
                       'form': form, })
    return HttpResponseRedirect('/')


def approve_reimbursement(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    if request.user:
        reinbursement = Reimbursement.objects.get(pk=pk)
        reinbursement.status = 'Approved'
        reinbursement.approved_date = datetime.today().date()
        reinbursement.save()
        return HttpResponseRedirect('/admin/employee_attendance/reimbursement/')
    return HttpResponseRedirect('/')


def availed_reimbursement(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    if request.user:
        reinbursement = Reimbursement.objects.get(pk=pk)
        reinbursement.status = 'Availed'
        reinbursement.approved_date = datetime.today().date()
        reinbursement.save()
        return HttpResponseRedirect('/admin/employee_attendance/reimbursement/')
    return HttpResponseRedirect('/')


def upload_resume(request):
    messages.info(request, "Upload function")
    import re
    if request.method=='POST':
        name = str( request.POST.get( "name" ) ).strip()
        email = request.POST.get( "Email__c" )
        contact = request.POST.get( "Contact_Number__c" )
        resume = request.FILES["resumeFile"]
        designation = request.POST.get( "Designation__c" )

        if not name or name=="" or not bool( re.match( '^[a-zA-Z ]+$', name ) ):
            messages.error( request, "Error: Name field must contains only Characters" )
            sf = SFConnectAPI()
            designations = ['Developer', 'Consultant', 'HR', 'QA', 'Bussiness Developer Executive', 'Content Writer', 'UI Developer', 'Sales Executive', 'Web Developer', 'Sales']
            return render( request,
                           "form.html", {'designations': designations,
                                                    'designation': designation,
                                                    'email': email,
                                                    "contact": contact,
                                                    "resume": resume,
                                                    } )

        elif not re.match( '^[0-9]+$', contact ) or len( contact )!=10:
            sf = SFConnectAPI()
            designations = ['Developer', 'Consultant', 'HR', 'QA', 'Bussiness Developer Executive', 'Content Writer', 'UI Developer', 'Sales Executive', 'Web Developer', 'Sales']
            messages.error( request, "Error: Phone field must contains only Numbers and length should be 10" )
            return render( request,
                           "form.html", {'designations': designations,
                                                    'designation': designation,
                                                    'email': email,
                                                    "contact": contact,
                                                    "resume": resume,
                                                    } )
    return HttpResponseRedirect('/')