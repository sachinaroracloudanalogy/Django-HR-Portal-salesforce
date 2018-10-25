from table import Table
from table.columns import Column, DatetimeColumn
from .models import Leave, Attendance, Reimbursement


class LeavesTable(Table):
    apply_date = Column(field='apply_date', header='Date')
    type_of_leave = Column(field='type_of_leave', header='Type')
    type_of_transaction = Column(field='type_of_transaction', header='Transaction')
    reason_for_leave = Column(field='reason_for_leave', header='Reason')
    remarks = Column(field='remarks', header='Remarks')
    leave_from = Column(field='leave_from', header='From')
    leave_to = Column(field='leave_to', header='To')
    leave_days = Column(field='leave_days', header='Total days')
    status = Column(field='status', header='status')

    class Meta:
        model = Leave


class AttendanceTable(Table):
    date__c = Column(field='date__c', header='Date')
    in_time__c = Column(field='in_time__c', header='In Time')
    out_time__c = Column(field='out_time__c', header='Out Time')


class HolidayTable(Table):
    date = Column(field='date', header='Date')
    description = Column(field='description', header = 'Description')


class ReimbursementTable(Table):
    billing_date = Column(field='billing_date', header='Date')
    type = Column(field='type', header='Type')
    amount = Column(field='amount', header='amount')
    applied_date = Column( field='applied_date', header='Date' )
    status = Column(field='status', header='status')

    class Meta:
        model = Reimbursement