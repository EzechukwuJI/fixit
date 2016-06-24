from fixitMain.models  import JobCategories, SubCategories, PostedJob, JobUploads, Responses
from fixitMain.models import Country, State, Zone, Area 
from fixitTradesmen.models import Biodata, CoporateData, Documents, Tradesman
from django import forms
from django.contrib.auth.models import User
from fixitMain.callables import get_content_tuple
import datetime




class LoginForm(forms.ModelForm):
	email = forms.EmailField(max_length = 128, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right','placeholder': 'Email','autofocus':'autofocus','required':'required'}))

	password = forms.CharField(max_length=10,required=True, widget=forms.PasswordInput
		(attrs={'class' : 'form-control formtext pull-right','placeholder':'Password','required':'required'}))
	
	class Meta:
		# Associate form with a model
		model = User
		fields = ('email','password',)



class JobUploadsForm(forms.ModelForm):
	
	picture  =  forms.ImageField(help_text="", widget=forms.FileInput(attrs={'class':'text-normal','id':'proj_pic','style':'font-size:12px;'}))
	document =  forms.ImageField(help_text="", widget=forms.FileInput(attrs={'class':'text-normal','id':'proj_doc','style':'font-size:12px;'}))

	class Meta:
		# Associate form with a model
		model = JobUploads
		fields = ('picture','document',)


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
		


class BioDataForm(forms.ModelForm):
	first_name = forms.CharField(max_length = 50, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right','placeholder': 'First Name'}))

	last_name = forms.CharField(max_length = 50, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'placeholder': 'Last Name'}))

	email = forms.EmailField(max_length = 50, help_text = "", widget=forms.EmailInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Email..'}))

	username = forms.CharField(max_length = 50, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Username'}))

	class Meta:
		model = User
		fields  = ["username", "email", "first_name","last_name"]








# class TradesmanPersonalForm(forms.ModelForm):
# 	address = forms.CharField(help_text = "", widget=forms.TextInput
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Address...','style':'width:75%;'}))

# 	phone_no = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Phone Number','style':'width:75%;'}))

# 	state = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'State','style':'width:75%;'}))

# 	city = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'City','style':'width:75%;'}))

# 	LGA = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Local government Area','style':'width:75%;'}))

# 	country = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Country','style':'width:75%;'}))

# 	passport  =  forms.ImageField(help_text="", label = 'Upload your picture', widget=forms.FileInput(attrs={'class':'text-normal pull-right','id':'proj_pic','style':'font-size:15px;'}))


# 	class Meta:
# 		model = Biodata
# 		fields = ['address','phone_no', 'state','city','LGA', 'country','passport']





# Not in use
# class BusinessDataForm(forms.ModelForm):
# 	company_name = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Name of Company (business Name)','style':'width:75%;'}))
# 	logo  =  forms.ImageField(help_text="upload business logo", label = 'Upload Company logo', widget=forms.FileInput(attrs={'class':'text-normal pull-right','id':'proj_pic','style':'font-size:15px;'}))
# 	sales_pitch = forms.CharField(max_length = 250, help_text = "", widget=forms.Textarea
# 		(attrs={'class':'form-control formtext pull-right', 'required':True, 'rows': 4, 'placeholder': 'Briefly describe what you do. (eg. We are the best in the building of..... etc.)','style':'width:75%;'}))

# 	class Meta:
# 		model = CoporateData
# 		fields = ['company_name','sales_pitch','logo']





SUBSCRIPTION_TYPE = (
	('Regular', 'Regular'),
	('PAYE', 'PAYE'),
	)





class CorporateDataForm(forms.ModelForm):
	company_name = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Name of Company (business Name)'}))

	company_logo  =  forms.ImageField(help_text="", label = 'Upload Company logo', widget=forms.FileInput(attrs={'style':'font-size:12px;', 'class':'pull-right'}))

	# category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Category'}), choices = get_content_tuple(JobCategories))

	category = forms.ModelChoiceField(queryset =  JobCategories.objects.all(), empty_label = "select category", to_field_name = "title_slug", 
	widget=forms.Select(attrs={'class':'form-control formtext pull-right', 'required':True }))

	# sub_category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Sub Category'}))


	# sub_category = forms.ModelChoiceField(queryset = SubCategories.objects.all(), widget=forms.Select(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Sub Category'}))
	# sub_category = forms.ModelChoiceField(queryset = SubCategories.objects.all(), widget=forms.Select(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Sub Category'}))

	sales_pitch = forms.CharField(max_length = 250, help_text = "", widget=forms.Textarea
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'rows': 4, 'placeholder': 'Briefly describe what you do. (eg. We are the best in the building of... etc.)'}))

	address = forms.CharField(help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Official Address'}))

	phone_no = forms.CharField(max_length = 25, help_text = "", widget=forms.NumberInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Phone Number'}))

	state = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'State'}))

	# city = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
		# (attrs={'class':'form-control formtext', 'required':True, 'placeholder': 'City'}))

	LGA = forms.CharField(max_length = 25, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Local government Area'}))

	country = forms.CharField(max_length = 25, help_text = "", widget=forms.TextInput
		(attrs={'class':'form-control formtext pull-right', 'required':True, 'placeholder': 'Country'}))

	passport  =  forms.ImageField(help_text="", label = 'Upload your picture', widget=forms.FileInput(attrs={'id':'proj_pic','style':'font-size:12px;', 'class':'pull-right'}))


	class Meta:
		model = Tradesman
		fields = ["company_name", "category","sales_pitch","address", "phone_no", "country", "state","LGA", "passport","company_logo" ]

		# fields = ["company_name", "category" , "sub_category", "sales_pitch","address", "phone_no", "country", "state","LGA", "passport" ]
		# excludes = ("user",)



