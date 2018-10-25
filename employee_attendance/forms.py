from django import forms
from .models import Employee, Leave, TRANSACTION_CHOICES, Reimbursement, REIMBURSEMENT_CHOICES, ReimbursementType
from bootstrap_daterangepicker import widgets, fields
from bootstrap_datepicker.widgets import DatePicker


class LogInForm( forms.ModelForm ):
    username = forms.CharField(widget=forms.TextInput, required=True, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=30)

    class Meta():
        model = Employee
        fields = ['username', 'password']


class DateRangeForm(forms.Form):
    date_range_with_format = fields.DateRangeField(
        widget=widgets.DateRangeWidget())
    # username = forms.CharField( widget=forms.TextInput, required=True, max_length=30 )



class LeaveForm(forms.ModelForm):
    type_of_leave = forms.CharField(widget=forms.TextInput, required=True, max_length=30, label="Leave Subject")
    type_of_transaction = forms.ChoiceField(widget=forms.Select, choices = TRANSACTION_CHOICES, required=True)
    leave_dates = fields.DateRangeField(input_formats=['%Y/%m/%d'], widget=widgets.DateRangeWidget(format='%Y/%m/%d'))
    # reason_for_leave = forms.CharField(widget=forms.TextInput, required=True, max_length=100)
    remarks = forms.CharField(widget=forms.Textarea, required=True, max_length=100,label='Description')

    class Meta():
        model = Leave
        fields = ['type_of_leave', 'type_of_transaction', 'remarks']


class ReimbursementForm(forms.ModelForm):
    billing_date = forms.DateField(widget=DatePicker(options={"format": "mm/dd/yyyy",
                                                              "autoclose": True}),
                                   required=True)
    type = forms.ModelChoiceField(queryset=ReimbursementType.objects.all())
    amount = forms.DecimalField(widget=forms.NumberInput, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True, max_length=500)

    class Meta():
        model = Reimbursement
        fields = ['billing_date', 'type', 'amount', 'description']
