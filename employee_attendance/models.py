"""
    This is the main model class of attendance app
"""
import datetime
from django.db import models

#  Opening Balance/Granted/Availed/Encashed/Lapsed/Closing Balance

TRANSACTION_CHOICES = (
    ('Opening Balance', 'Opening Balance'),
    ('Granted', 'Granted'),
    ('Availed', 'Availed'),
    ('Encashed', 'Encashed'),
    ('Lapsed', 'Lapsed'),
    ('Closing Balance', 'Closing Balance'),
)

REIMBURSEMENT_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Availed', 'Availed'),
)

ROLE_CHOICES = (
    ('Super Admin', 'Super Admin'),
    ('Admin HR', 'Admin HR'),
    ('Admin', 'Admin'),
    ('Project Manager', 'Project Manager'),
    ('Team Lead','Team Lead'),
    ('Developer','Developer'),
    ('Intern Developer','Intern Developer'),
    ('QA or Tester', 'QA or Tester'),
)


class Employee(models.Model):
    """
        This class contains the Fields of Employee Information module
    """
    record_id = models.CharField( max_length=15, null=True, blank=True )
    employee_id = models.CharField(max_length=30, blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    username = models.CharField(max_length=30, blank=False, unique=True)
    password = models.CharField(max_length=12, blank=False)
    dob = models.DateField(blank=False)
    designation = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=False)
    address = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.first_name)

    class Meta:
        verbose_name_plural = 'Employee'
        verbose_name = 'Employees'


class Attendance(models.Model):
    """
        This class contains the Fields of Attendance module
    """
    record_id = models.CharField(max_length=15, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    ca_emp_in_time = models.DateTimeField()
    ca_emp_out_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.date

    class Meta:
        verbose_name_plural = 'Attendance'
        verbose_name = 'Attendances'


class Log(models.Model):
    """
        This class contains the Fields of Login System module
    """
    record_id = models.CharField( max_length=15, null=True, blank=True )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    in_time = models.DateTimeField()
    out_time = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.employee) + str(self.in_time) + str(self.out_time)

    class Meta:
        verbose_name_plural = 'Log'
        verbose_name = 'Logs'


class Leave(models.Model):
    """
        This class contains the Fields of Leave module
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type_of_leave = models.CharField(max_length=30, blank=False, null=True)
    type_of_transaction = models.CharField(max_length=30, choices=TRANSACTION_CHOICES,
                                           blank=False, null=True)
    leave_from = models.DateField(null=True)
    leave_to = models.DateField(null=True)
    leave_days = models.IntegerField(null=True)
    reason_for_leave = models.CharField(max_length=100, blank=False, null=True)
    remarks = models.CharField(max_length=256, null=True)
    apply_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=30, blank=False, default='applied')

    def __str__(self):
        return str(self.employee) + str(self.leave_from)

    class Meta:
        verbose_name_plural = 'Leave'
        verbose_name = 'Leaves'


class Holiday(models.Model):
    """
        This class contains the Fields of Holiday module
    """
    date = models.DateField()
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.date + self.description

    class Meta:
        verbose_name_plural = 'Holiday'
        verbose_name = 'Holidays'


class ReimbursementType(models.Model):
    """
        This class contains TYPES OF Reimbursement
    """
    type_name = models.CharField(max_length=256, null=True, unique=True)
    description = models.TextField(max_length=256, null=True)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name_plural = 'Reimbursement Type'
        verbose_name = 'Reimbursement Types'


class Reimbursement(models.Model):
    """
         This class contains the Fields of Reimbursement module
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)
    billing_date = models.DateField(default=datetime.date.today, null=False, blank=False,)
    type = models.ForeignKey(ReimbursementType, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    bill = models.ImageField()
    description = models.TextField( max_length=500, null=True, blank=True )
    status = models.TextField(max_length=256, null=False, choices=REIMBURSEMENT_CHOICES)
    applied_date = models.DateField(default=datetime.date.today)
    approved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.employee) + str(self.applied_date)

    class Meta:
        verbose_name_plural = 'Reimbursement'
        verbose_name = 'Reimbursements'
