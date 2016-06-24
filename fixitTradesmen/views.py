from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import F
from django.http import HttpResponse

from fixit.settings import DOMAIN_PREFIX
from fixitCustomers.models import Customers as cust
from fixitMain.callables import get_Responses, DisplayRating
from fixitTradesmen.models import Biodata, CoporateData, Documents, Tradesman
from fixitMain.models import PostedJob as jobs 
from fixitMain.models   import Responses, Zone, JobCategories, SubCategories

from fixitMain.forms import JobResponseForm, BioDataForm,CorporateDataForm
# TradesmanPersonalForm,

from fixitCustomers.models import Customers as cust
from fixitMain.user_permission_test import is_tradesman

from fixitMain.callables import pGen,get_UserID 

from django.views.generic import View
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView



# def tradesmanRegView(request, source):
# 	context = {}
# 	if request.user.is_authenticated:
# 		logout(request)

# 	bio    = TradesmanBioForm()
# 	biz    = BusinessDataForm()
# 	trade  = TradesmanPersonalForm()

# 	context['bioform']  		=   bio
# 	context['bizform']  		=   biz
# 	context['personalform']     =   trade
# 	context['categories']       =   JobCategories.objects.all()

# 	 # check preceeding action  
# 	if source == "response":
# 		logout(request)
# 		return redirect(reverse('fixitMain:login'))

# 	if request.method == "POST":
# 		bio    = 	TradesmanBioForm(data = request.POST)
# 		biz    = 	BusinessDataForm(data = request.POST)
# 		trade  = 	TradesmanPersonalForm(data = request.POST)
# 		bio.save()
# 		biz.save()
# 		trade.save()
# 		#  return registration form here
# 	return render(request, 'fixit/tradesmen/tradesman-register.html', context)







# class RegisterTradesmanView(CreateView):
# 	corporateForm   =    TradesmanForm
# 	BiodataForm     =    TradesmanBioForm
# 	# initial = {'key': 'value'}
# 	# model           =    Tradesman
# 	template_name   =    "fixit/tradesmen/tradesman-register.html"

# 	def get(self, request, *args, **kwargs):
# 		corporate_data    =    self.corporateForm()
# 		biodata_form      =    self.BiodataForm()
# 		categories        =    JobCategories.objects.all()
# 		return render (request, self.template_name, {'biodataform':biodata_form, 'corporate_form':corporate_data, 'categories':categories})


# 	# def form_valid(self, form):
# 	# 	print "Form validation in progress ....."
# 	# 	# form = self.corporateForm(request.POST, request.FILES)
# 	# 	# # corporate
# 	# 	form.instance.category     =   JobCategories.objects.get(title_slug = self.request.POST.get('category'))
# 	# 	# form.instance.sub_category =   SubCategories.objects.get(title_slug = self.request.POST.get('sub_category'))
# 	# 	return super(RegisterTradesmanView, self).form_valid(form)
# 	def post(self, request, *args, **kwargs):	
# 		biodata_form      =    self.BiodataForm(request.POST)
# 		corporate_data    =    self.corporateForm(request.POST, request.FILES)

# 		if biodata_form.is_valid() and corporate_data.is_valid():
# 			# corporate_data = corporate.save(commit = False)
# 			# biodata.save(commit = False)
# 			print "Form processing got here..."
# 			# corporate_data.category = JobCategories.objects.get(title_slug = request.POST.get('category'))
# 			# corporate_data.sub_category = SubCategories.objects.get(title_slug = request.POST.get('sub_category'))
# 			# corporate_data.save()
# 			# user = biodata.save()
# 			# user.set_password(pGen())
# 			# user.save()
# 			# print "form is valid"
# 			return HttpResponse("success")
# 		else:
# 			print biodata_form.errors
# 			print corporate_data.errors
# 		return render(request, self.template_name, {'biodataform':biodata_form, 'corporate_form':corporate_data})






def RegisterTradesmanView(request, **kwargs):
	# logout user if logged in
	logout(request)
	corporate_data_form     =    CorporateDataForm()
	biodata_form        	=    BioDataForm()
	template_name       	=    "fixit/tradesmen/tradesman-register.html"
	uniqueID            	=    get_UserID(Biodata) + "t"
	categories          	=    JobCategories.objects.all()
	user_password           =    pGen()
	if request.method == "POST":
		rp = request.POST
		corporatedata   			    =   CorporateDataForm(request.POST, request.FILES)
		biodata         			    =   BioDataForm(request.POST, request.FILES)
		
		if corporate_data_form.is_valid and biodata_form.is_valid:
			#  check unique registration
			if User.objects.filter(email = rp['email']).exists():
				messages.error(request, "Sorry that email is already in use on this site, Please enter another")
				return render(request, template_name, {'biodataform':biodata, 'corporate_form':corporatedata, 'categories':categories})
			# elif User.objects.filter(username = rp['username']).exists():
			# 	messages.error(request, "Sorry that username is already in use on this site, Please enter another")
			# 	return render(request, template_name, {'biodataform':biodata, 'corporate_form':corporatedata, 'categories':categories})

			coporate_info   			=   corporatedata.save(commit=False)
			coporate_info.category      =   JobCategories.objects.get(title_slug = rp['category'])
			coporate_info.sub_category  =   SubCategories.objects.get(title_slug = rp['sub_category'])
			user                        =   User.objects.create(first_name = rp['first_name'],
				last_name=rp['last_name'],email=rp['email'],username=rp['email'])
			user.set_password(user_password)
			coporate_info.userID        =   uniqueID
			coporate_info.user          =   user

			g = Group.objects.get(name = 'Tradesman')
			g.user_set.add(user)

			user.save()
			coporate_info.save()

			# send login details to user
			link = DOMAIN_PREFIX + "/account/profile/"
			print "login link ", link
			print "password ", user_password
			# SEND MAIL WITH PASSWORD using sendmail
			message  = "Hello " + rp['first_name'].title() 
			message += ", <br/><br/> Thank you for signing up on " + DOMAIN_PREFIX + " <br/> Log into your account with your details below and "
			message += "start submitting bids for as many projects as you can. <br/><br/> You are required to change this password once you're logged in.<br/>"
			message += "Use the link below to change your password.<br/>"
			message += "<br/><strong> Your logging details are: </strong> <br/><br/> Username: " + rp['email'] + "<br/>password: " + str(user_password) + "<br/><br/>"
			message += "Change your password  <a href=" + str(link) + ">Here</a> <br/> <br/><br/> Yours in Service, <br/> The " + DOMAIN_PREFIX + " Team"
			# send email to customer
			notify  = EmailMessage(subject= '[Ndoozi] Your account has been created successfully', body = message, to =[rp['email']])
			notify.content_subtype = 'html'
			notify.send()

			# messages.success(request, "Your account has been created, check your mailbox to get your login details")
			return redirect(reverse('fixitMain:signup_success', kwargs = {'userID': uniqueID }))
		else:
			messages.error(request, "error encountered")
			return render(request, template_name, {'biodataform':biodata, 'corporate_form':corporatedata, 'categories':categories})
	return render(request, template_name, {'biodataform':biodata_form, 'corporate_form':corporate_data_form,'categories':categories })






@login_required()
def tradesmanAccountView(request):
	context = {}
	user = request.user
	if not user.groups.filter(name = 'Tradesman').exists(): #use user permissions for this
		logout(request)
		messages.info(request, "Sorry! you do not have the permission to view the page you tried to access.")
		return redirect(reverse('fixitMain:login'))
	else:
		return render(request, 'fixit/tradesmen/tradesman-account.html', {})
	
	






def tradesmanVerifyView(request):
	return render(request, 'fixit/tradesmen/tradesman-verification.html', {})





@login_required()
def tradesmanProfileView(request, user_id):
	context = {}
	# Get job Id from job view sessions
	## from customer job details and general job details page

	# Fix issue.... "no session variable" on logout
	tradesman             =    get_object_or_404(Tradesman, userID = user_id)

	job_id                =    request.session.get('job_in_view')
	cust_job_view_id      =    request.session.get('cust_job_view_session')
	try:
		job_in_view       =     get_object_or_404(jobs, job_id = job_id)
	except:
		job_in_view       =    get_object_or_404(jobs, job_id = cust_job_view_id)
	context['id']         =    job_id
	context['category']   =    job_in_view.job_category.title_slug
	context['title']      =    job_in_view.title_slug 

	# Verify that profile viewer is the owner of job responded to
	# Prevent anonymous profile view
	try:
		if not job_in_view.postedby ==  cust.objects.get(customer__email = request.user.email):
			messages.info(request,"you cannot view this profile Think about how to send the message accross")
			return redirect(reverse('fixitMain:job_details', kwargs = context)) # send a signal for user notification
		# Complete the view restrictions here
	except:
		return redirect(reverse('fixitMain:job_details', kwargs = context))
	output                       =    {}
	context['reviews']           =    jobs.objects.filter(taken_by  =  tradesman.user.email, status = "Closed")
	context['display_rating']    =    DisplayRating(tradesman.user.email)[0]
	try:
		if Tradesman.objects.filter(userID=user_id).exists():
			tradesman_in_view    =     Tradesman.objects.get(userID = user_id)
			# coporatedata          =     CoporateData.objects.get(user__userID = user_id)
		else:
			biodata               =     {}
			coporatedata          =     {}
			context['notfound']   =     True
		context['userinfo']       =     tradesman_in_view
		# context['bizinfo']        =     coporatedata
	except:
		# print "Details not found for %s" %(user_id)
		return render(request, 'fixit/tradesmen/tradesman-profile.html', context)
	else:
		return render(request, 'fixit/tradesmen/tradesman-profile.html', context)





@login_required()
# @user_passes_test(is_tradesman, login_url='/login/', redirect_field_name = None)
def jobResponseView(request, pid, title, action):
	if not user_passes_test(is_tradesman):
		return redirect(reverse('fixitMain:all-jobs'))
	else:
		context                   =      {}
		form                      =      JobResponseForm()
		context['form']           =      form
		this_job                  =      jobs.objects.get(job_id  =   pid, title_slug = title)
		context['job']            =      this_job
		context['zones']          =      Zone.objects.all()
	# prevent multiple responses per tradesman per job
	for responses in get_Responses(this_job.job_id):
		if request.user.email in responses.responder:
			context['responded']  =   True
			break
	return render(request, 'fixit/tradesmen/job_response.html', context)







@login_required()
def saveJobResponse(request):
	if request.method == 'POST':
		job_id               =      request.POST.get('job_id').strip()
		job_title            =      request.POST.get('job_title').strip()
		responder_email      =      request.POST.get('responder').strip()
		this_job             =      jobs.objects.get(job_id  =   job_id, title_slug = job_title)

		new_response         =   Responses.objects.create(job_id = this_job, responder = responder_email, 
			response_note    =   request.POST.get('response_note'), quoted_amount = request.POST.get('quoted_amount'),
			supply_estimate  =   request.POST.get('supply_estimate'), supply_list = request.POST.get('supply_list'))

		jobs.objects.filter(job_id = job_id, title_slug = job_title).update(num_response= F('num_response') + 1)

		# Notify job owner about response to job 
		link       =   DOMAIN_PREFIX + "/customer/myjobs/" + job_id
		jobs.objects.filter(job_id = job_id, title_slug = job_title).update(num_response= F('num_response') + 1)

		# jobs.objects.filter(job_id = job_id, title_slug = job_title).update(
		# 	num_response = response_count + 1
		# 	)

		# Notify job owner about response to job 
		# link       =   "www.ndoozi.com/customer/myjobs/" + job_id

		job_owner  =   cust.objects.get(customer__email = this_job.postedby.customer.email)

		message = "Hello " + job_owner.customer.first_name.title() 
		message += ", <br/> A specialist has submitted a quotation for your job <strong><u> " + job_title 
		message += "</u></strong> on" + DOMAIN_PREFIX + ". Click the attached link below to log into your account and view this response."
		message += "<br/><br/><br/>" + link 
		message += "<br/> <br/> Yours in service: <br/> The ndoozi.com Team"
		
		notify  = EmailMessage(subject= 'People Are Responding To Your Job', body = message, to =[job_owner.customer.email])
		notify.content_subtype = 'html'
		notify.send()
	return redirect(reverse('fixitMain:all-jobs'))









def howItWorksView(request):
	return render(request, 'fixit/tradesmen/how-it-works.html', {})



def pricingView(request):
	return render(request, 'fixit/tradesmen/pricing.html', {})
