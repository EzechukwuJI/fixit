import datetime
import string

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt, csrf_protect

from fixitMain.models import Responses, JobUploads, Zone, State, Area, Country
from fixitMain.forms import JobUploadsForm

from fixit.settings import DOMAIN_PREFIX
from fixitMain.models import PostedJob 
from fixitCustomers.models import Customers as C
from fixitMain.models import Messages
from fixitTradesmen.models import Tradesman #CoporateData, Biodata
from fixitTradesmen.models import JobList as T_joblist
from fixitMain.callables import get_Responses, paginate_list, rateJobPerformance, \
pGen,get_TradesmanRating, retrieveMessages, get_UserID 
# Registration_code
from fixitCustomers.forms import CustomerEditForm




def custRegForm(request, source=None, ref = None):
	if request.user.is_authenticated:
		logout(request)
	context                    =      {}
	context['states']          =      State.objects.all()
	context['countries']       =      Country.objects.all()
	if source == "new" or ref == 1:
		return render(request, 'fixit/customers/register-customer.html', context)
	elif source                             ==        "post-project":
		user_string = ref.split('-')
		context['email']                    =          user_string[1]
		context['fname']                    =          user_string[2]
		if user_string[0]                   ==         "c":
			context['new_user']             =          True
		elif user_string[0]                 ==         't':
			context['tradesman']            =          True
		return render(request, 'fixit/main/post-job.html', context)






def custSignUp(request):
	context  = {}
	email = ""
	if request.method   == 'POST':
		email           =     request.POST.get('email').strip()
		# check email exists
		if C.objects.filter(customer__email = email).exists() or User.objects.filter(username = email).exists():  
			context['email_taken']  =  True
			return render(request, 'fixit/customers/register-customer.html', context)

		first_name      =     request.POST.get('fname').strip()
		address         =     request.POST.get('address').strip()
		phone           =     request.POST.get('phone_number').strip()
		state           =     request.POST.get('state').strip()
		area            =     request.POST.get('area').strip()
		country         =     request.POST.get('country').strip() 
		password        =     pGen()
		uniqueID        =     get_UserID(C) + "c"
		# registration_code =   Registration_code()

		new_user = User.objects.create(username = email, first_name = first_name, email = email)

		user = get_object_or_404(User, email = new_user.email)
		user.set_password(password)

		# Assign user to user group
		g = Group.objects.get(name = 'Regular')
		g.user_set.add(user)
		user.save()
		
		# print "User and password", user, "  :", password
		message = ""
		new_customer = C.objects.create(userID = uniqueID, customer = new_user, address = address, city = 'city',
			state = state, area= area, country = country, phone_no = phone, account_type = 'Regular')
		link = DOMAIN_PREFIX + "/accounts/profile/"
		print "login link ", link
		print "password ", password
		# SEND MAIL WITH PASSWORD using sendmail
		message  = "Hello " + first_name.title() 
		message += ", <br/><br/> Thank you for signing up on " + DOMAIN_PREFIX + " <br/> Log into your account with your details below and "
		message += "start posting your projects. <br/><br/> You are required to change this password once you're logged in.<br/>"
		message += "Use the link below to change your password.<br/>"
		message += "<br/><strong> Your logging details are: </strong> <br/><br/> Username: " + email + "<br/>password: " + str(password) + "<br/><br/>"
		message += "Change your password  <a href=" + link + ">Here </a><br/> <br/><br/> Yours in Service, <br/> The " + DOMAIN_PREFIX + " Team"
		# send email to customer
		notify  = EmailMessage(subject= '[Ndoozi] Your account has been created successfully', body = message, to =[email])
		notify.content_subtype = 'html'
		notify.send()
	# email           =     request.POST.get('email')
	if  request.POST.get('sent_from')      ==  'post_project':
		return redirect(reverse('fixitMain:postjob', kwargs = {'category': 'new' }))
	elif request.POST.get('sent_from')     ==     'signup_form':
		return redirect(reverse('fixitMain:signup_success', kwargs = {'userID': uniqueID }))
	return redirect(reverse('fixitMain:signup_success', kwargs = {'userID': uniqueID }))








@login_required()
def custAccountView(request):
	context   = {}
	user = request.user
	if not user.groups.filter(name = 'Regular').exists():
		# print "Not a customer"
		logout(request)
		# context['is_tradesman'] = True  #Implement this later
		messages.info(request, "Sorry! you do not have the permission to view the page you tried to access.")
		return redirect(reverse('fixitMain:login'))
	else:
		this_user  =  get_object_or_404(C, customer__email = user.email)
		context['current_user']  = this_user
	return render(request, 'fixit/customers/my-account.html', context)







@login_required()
def custJobDetailView(request, job_id):
	context     =       {}
	responders  =  		[]

	# Create a session for the job in view
	request.session['cust_job_view_session'] = job_id
	responses = get_Responses(job_id)
	for response in responses:
		# Get alll the tradesmen that responded to this job
		responder = Tradesman.objects.get(user__email = response.responder)  # change email to ID
		# responder = CoporateData.objects.get(user__tradesman__email = response.responder)  # change email to ID
		responders.append(responder)
	# print "responders to this ", responders
	this_job       =    get_object_or_404(PostedJob, job_id =job_id)
	if not this_job.status  == 'Open':
		context['job_is_taken']       =     True
	# context['job'] = PostedJob.objects.get(job_id  =  job_id)
	context['job']                 =     this_job
	context['responses']           =     responses
	context['responders']          =     responders
	context['uploads_form']        =     JobUploadsForm()
	context['messages']            =     retrieveMessages(job_id, this_job.postedby.customer.email)	
	return render(request, 'fixit/customers/cust_job_detail.html', context)





@login_required()
def custMyjobsView(request):
	context   =   {}
	if request.user.is_authenticated():
		#Get jobs posted by customers
		myjobs = PostedJob.objects.filter(postedby__customer__email = request.user.email) #change email to user ID
		print "user email ", request.user.email
		print "My jobs " , myjobs
		context['myjobs']  = myjobs
	return render(request, 'fixit/customers/my-jobs.html', context)





@login_required()
def jobEditView(request, job_id):
	context   =    {}
	context['job_id']    = job_id
	if request.method == "POST":
		title          =   request.POST.get('new_title').strip()
		description    =   request.POST.get('new_description').strip()
		startdate      =   request.POST.get('select_startdate')
		budget         =   request.POST.get('project_budget')
		duration       =   request.POST.get('time_frame')
		if title == "" or description =="" or startdate =="" or budget == "" or duration == "":
			return redirect(reverse('fixitCustomers:job_details', kwargs = context ))
		else:
			PostedJob.objects.filter(job_id = job_id).update(
				job_title = title,description = description, start_date = startdate, 
				budget = budget, time_frame = duration, edited_on = datetime.datetime.now())
	return redirect(reverse('fixitCustomers:job_details', kwargs = context))

	
	




@login_required()
@csrf_exempt
def editProfileView(request):
	context   =    {}
	context['edit']   =   True
	editForm    =    CustomerEditForm()
	
	if request.method == "POST":
		address    =   request.POST.get('currentaddress').strip()
		city       =   request.POST.get('currentcity').strip()
		state      =   request.POST.get('new_state').strip()
		phone_no   =   request.POST.get('new_phone').strip()
		if address == "" or city =="" or state =="" or phone_no == "":
			return redirect(reverse('fixitCustomers:my-account'))
		else:
			C.objects.filter(customer__username = request.user.username).update(
				address = address,city = city, state = state, phone_no = phone_no)
	return redirect(reverse('fixitCustomers:my-account'))














@login_required()
def acceptTradesmanView (request, job_id, tradesman):
	context      =       {}
	# Get selected tradesman's email address
	tradesman         =     get_object_or_404(Tradesman, userID = tradesman)
	# tradesman         =     get_object_or_404(CoporateData, user__user_id = tradesman)
	job       =  get_object_or_404(PostedJob, job_id = job_id)
	tradesmans_email  =  tradesman.user.email
	# Add job to tradesmans Joblist
	new_tradesman_list      =     T_joblist.objects.create(
		tradesman =  tradesman, # get_object_or_404(CoporateData, user__user_id = tradesman),
		job       =  job,    #get_object_or_404(PostedJob, job_id = job_id),
		rating    =  0, 
		status    =  "In Progress",
		fee       =  Responses.objects.get(job_id__job_id = job_id, responder = tradesmans_email).quoted_amount )
	# Update project status
	PostedJob.objects.filter(job_id = job_id).update(
		status = "In Progress", taken_by = tradesmans_email)
	context['T_accepted']        =    True
	context['job_id']            =    job_id

	link  =   DOMAIN_PREFIX + "/accounts/login/"
	# send mail to accepted tradesman
	
	print "tradesman email", tradesmans_email
	message = "<div style='background-color: #e0e0e0; border-top: 2px solid #000000; padding: 10px; width: 50%; margin-top:4%;'>"
	message += "<strong> Hello </strong> " + tradesman.user.first_name +","
	message += " " 
	message += "<br/><br/> We are pleased to inform you that a customer, on our platform has chosen your company <br/>"
	message += "<strong>" + tradesman.company_name + "</strong>, as the preferred bidder."
	message += "for the execution of the project <strong> " + job.job_title + " </strong><br/>Kindly log into your account on www.ndoozi.com <br/>"
	message += "with the link below, to finalize your arrangements with this client. <br/> <i> Congratulation. </i><br/><br/> "
	message += link + " <br/><br/>"
	message += "Regards: <br/> The ndoozi.com Team <br/><small class='text-warning'>your partner in Progress</small> </div>"

	notify  = EmailMessage(subject= "A Client has chosen you", body = message, to =[tradesmans_email])
	notify.content_subtype = 'html'
	notify.send(fail_silently = False) # this will be activated when before going live

	# print "Email ", message
	# return HttpResponse(message)
	return redirect(reverse('fixitCustomers:job_details', kwargs = {'job_id': job_id }))





@login_required()
def  rate_Close_JobView(request, job_id):
	context                  =   {}
	score_list               =   []
	job                      =   get_object_or_404(PostedJob, job_id = job_id)
	context['job_id']        =   job_id
	context["job_title"]     =   job.job_title
	#  check job response  and acceptance status
	if job.num_response         !=   0 and job.taken_by != " ":
		tradesman_email          =   job.taken_by
		tradesman                =   Tradesman.objects.get(user__email = tradesman_email)
		# tradesman                =   CoporateData.objects.get(user__tradesman__email = tradesman_email)
		context['tradesman']     =   tradesman.company_name
		tradesman_jobs_count     =   tradesman.jobs_count

		if request.method == "POST":
			# score_list = [item for item in request.POST.__dict__ ]
			# print "score list ",score_list

			score_list = [request.POST['reliability'],request.POST['pricing'],request.POST['loyalty'],
			request.POST['craftmanship'],request.POST['relationship'],request.POST['within_budget']
			,request.POST['timely']]

			#  get job rating 
			job_rating = rateJobPerformance(score_list)
			# update trademans joblist
			T_joblist.objects.filter(tradesman__user__email = tradesman_email, job = job).update(
				rating          =   job_rating,
				status          =   "Closed",
				date_closed     =   datetime.date.today(),
				# fee             =   float(request.POST.get('final_cost')),
				review          =   request.POST.get('customer_comments').strip())
			# update jobs
			PostedJob.objects.filter(job_id = job_id).update(
				status    =    "Closed",
				review    =    request.POST.get('customer_comments').strip())

			tradesman_rating =  get_TradesmanRating(tradesman_email) # CHANGE THIS TO REFLECT RATE COUNT
			
			# update tradesmans rating 
			Tradesman.objects.filter(user__email = tradesman_email).update(
			# CoporateData.objects.filter(user__tradesman__email = tradesman_email).update(
				# rating = tradesman_rating ,
				jobs_count  = int(tradesman_jobs_count) + 1 
				)

			return redirect(reverse('fixitCustomers:my-jobs'))
		else:
			return render(request, 'fixit/Customers/job-closure.html', context)
			# PostedJob.objects.filter(job_id = job_id).update(
			# 	status    =    "Closed",
			# 	review    =    "None" )
			# return redirect(reverse('fixitCustomers:my-jobs'))
	else:
		context['no_tradesman']    =    True
		return render(request, 'fixit/Customers/job-closure.html', context)

	



def sendMessageView(request, job_id):
	job = get_object_or_404(PostedJob, job_id = job_id)
	sender = ""
	if request.user.email == job.postedby.customer.email:
		sender    =   get_object_or_404(User, email = request.user.email)  
	else:
		sender    =   get_object_or_404(User, email=job.taken_by)
	if request.method == "POST":
		new_message  =   Messages.objects.create(
			sent_from = sender,
			related_job = job,
			message = request.POST.get('message') 
			)
		print new_message
	return redirect(reverse('fixitCustomers:job_details', kwargs = {'job_id': job_id }))






@login_required()
def resetPasswordView(request):
	context = {}
	user = request.user
	if request.method == "POST":
		existing_pw = user.check_password(request.POST.get('oldpassword'))
		if existing_pw:
			user.set_password(request.POST.get('newpassword'))
			user.save()
			logout(request)
			return redirect(reverse('fixitMain:login'))
		else:
			this_user  =  get_object_or_404(C, customer__email = user.email)
			context['current_user']  = this_user
			context['incorrect_pw']   =    True
			return render(request, 'fixit/customers/my-account.html', context)
	return redirect(reverse('fixitCustomers:my-account'))
