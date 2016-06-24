from django import forms
from django.contrib.auth.models import User
from fixitCustomers.models import Customers

import datetime






class CustomerEditForm(forms.ModelForm):

	class Meta:
		model = Customers
		fields  =  '__all__'
