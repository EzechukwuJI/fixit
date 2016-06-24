from fixitMain.models  import JobCategories, SubCategories, PostedJob, JobUploads, Responses
from fixitMain.models import Country, State, Zone, Area 
from fixitTradesmen.models import Biodata, CoporateData, Documents, Tradesman
from django import forms
from django.contrib.auth.models import User
from fixitMain.callables import get_content_tuple
import datetime




class JobResponseForm(forms.ModelForm):
	job_id = forms.CharField(max_length = 13, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right','placeholder': 'ID','style':'width:75%;'}))

	responder = forms.CharField(max_length = 13, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right','placeholder': 'Tradesman','style':'width:75%;'}))

	response_note = forms.CharField(max_length = 200, help_text = " ",widget=forms.Textarea
		(attrs={'class':'form-control formtext pull-right','placeholder': 'Drop a message for the client','style':'width:75%; height:75px;'}))

	quoted_amount = forms.CharField(max_length = 13, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right','placeholder': 'Job quotation','style':'width:75%;'}))

	supply_estimate = forms.CharField(max_length = 13, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right','placeholder': 'Estimated cost of materials','style':'width:75%;'}))

	supply_list = forms.CharField(max_length = 350, help_text = "",widget=forms.Textarea
		(attrs={'class':'form-control formtext pull-right','placeholder': 'List of materials needed', 'style':'width:75%; height:75px;' }))

	class Meta:
		# Associate form with a model
		model = Responses
		fields = ()
		


class TradesmanBioForm(forms.ModelForm):
	firstname = forms.CharField(max_length = 50, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right','placeholder': 'First Name'}))

	last_name = forms.CharField(max_length = 50, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Last Name'}))

	email = forms.EmailField(max_length = 50, help_text = "", widget=forms.EmailInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Email..'}))

	username = forms.CharField(max_length = 50, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Username'}))

	class Meta:
		model = User
		fields  = ["username", "email", "firstname","last_name"]








class TradesmanPersonalForm(forms.ModelForm):
	address = forms.CharField(help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Address...','style':'width:75%;'}))

	phone_no = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Phone Number','style':'width:75%;'}))

	state = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'State','style':'width:75%;'}))

	city = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'City','style':'width:75%;'}))

	LGA = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Local government Area','style':'width:75%;'}))

	country = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Country','style':'width:75%;'}))

	passport  =  forms.ImageField(help_text="", label = 'Upload your picture', widget=forms.FileInput(attrs={'class':'text-normal pull-right','id':'proj_pic','style':'font-size:15px;'}))


	class Meta:
		model = Biodata
		fields = ['address','phone_no', 'state','city','LGA', 'country','passport']






class BusinessDataForm(forms.ModelForm):
	company_name = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Name of Company (business Name)','style':'width:75%;'}))
	logo  =  forms.ImageField(help_text="upload business logo", label = 'Upload Company logo', widget=forms.FileInput(attrs={'class':'text-normal pull-right','id':'proj_pic','style':'font-size:15px;'}))
	sales_pitch = forms.CharField(max_length = 250, help_text = "", widget=forms.Textarea
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'rows': 4, 'placeholder': 'Briefly describe what you do. (eg. We are the best in the building of..... etc.)','style':'width:75%;'}))

	class Meta:
		model = CoporateData
		fields = ['company_name','sales_pitch','logo']