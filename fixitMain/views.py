import string 

from django.shortcuts import render,redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.core import serializers
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

from fixitMain.models import JobCategories, SubCategories,PostedJob, State
from fixitMain.models import Responses,JobUploads, Zone, State, Area
from fixitMain.callables import get_Responses, paginate_list, processAjaxRequest 
from fixitMain.callables import get_JobID, get_zone, notify_tradesmen

from fixitMain.forms import LoginForm, JobUploadsForm
from django.contrib import messages
from fixitTradesmen.models import CoporateData, Tradesman
# from fixitTradesmen.models import Biodata as Tradesmen
from fixitCustomers.models import Customers

from fixit.settings import DOMAIN_PREFIX


from django.views.generic import TemplateView



# Create your views here.
def   mainIndexView(request):
    odd_list_dict       =     {} # odd numbered job categories
    even_list_dict      =     {} # Even numbered job categories
    context             =     {}
    categories          =     JobCategories.objects.all() # get all categories in db

    for cat in categories:
        if cat.id % 2:
            odd_list_dict[cat.title_slug]   = cat.category_title
        else:
            even_list_dict[cat.title_slug]  =  cat.category_title
    context  =  {
            'odd_list': odd_list_dict, 
            'even_list':even_list_dict, 
            'all_categories':categories 
            }
    context['num_categories']     =     JobCategories.objects.all().count();
    context['num_customers']      =     Customers.objects.all().count();
    context['num_tradesmen']      =     Tradesman.objects.all().count();
    context['num_jobs']           =     PostedJob.objects.all().count();

    # return render(request,  'fixit/main/index.html', context )

    return render(request,  'fixit/main/index.html', context )

    # return render(request,  'fixit/main/registration_success.html', context )






def signupSuccess (request, userID):
    model      =   object()
    context    =   {}
    useremail  =   ""
    username   =   ""
    user_type_initial = userID[-1]
    if user_type_initial == 'c':
        model = Customers
    elif user_type_initial  == 't':
        model = Tradesman
    new_user = get_object_or_404(model, userID = userID)
    if user_type_initial == "c":
        useremail = new_user.customer.email
        username  = new_user.customer.first_name
    else:
        useremail =    new_user.user.email
        username  =    new_user.user.first_name
    emailprovider = useremail[string.index(useremail, "@") + 1 : string.index(useremail,".")]
    context['username']         =  username
    context['emailprovider']    =  emailprovider
    context['useremail']        =  useremail

    # new_user = get_object_or_404(Tradesman, userID = userID)
    # useremail = new_user.customer.email
    # emailprovider = useremail[string.index(useremail, "@") + 1 : string.index(useremail,".")]
    # context = {}
    # context['username']         =  new_user.customer.first_name
    # context['emailprovider']    =  emailprovider
    # context['useremail']        =  new_user.customer.email

    return render(request, 'fixit/main/registration_success.html', context)




# def signupSuccess (request, useremail):
#     new_user = get_object_or_404(User, email = useremail)
#     emailprovider = new_user.email[string.index(new_user.email, "@") + 1 : string.index(new_user.email,".")]
#     context = {}
#     context['username'] = new_user.first_name
#     context['emailprovider'] = emailprovider
#     context['useremail']  =  useremail
#     return render(request, 'fixit/main/registration_success.html', context)





# @login_required()
def   displayJobForm(request, category):
    context        =      {}
    context['has_category']           =       False
    context                           =       {}
    if not category                   ==      "new":
        cate_in_view                  =        get_object_or_404(JobCategories, title_slug = category)
        category_caption              =        cate_in_view.caption
        # category_caption              =       get_object_or_404(JobCategories, title_slug = category).caption
        # subcategories                 =        
        # print "sub categories in ", category, " == ", subcategories
        # SubCategories.objects.filter()
        context['has_category']       =       True
        context['category_title']     =       cate_in_view.category_title
        context['subcategories']      =       cate_in_view.subcategories.all()
        # context['category_title']     =       JobCategories.objects.get(title_slug = category).category_title
    else:
        category_caption = "create your projects here"
        context['has_category']       =   False
    if request.method  ==  'POST':
        createNewProject(request)
    categories                =      JobCategories.objects.all()
    context['categories']     =      categories
    context['uploads_form']   =      JobUploadsForm
    context['caption']        =      category_caption
    return render(request,  'fixit/main/post-job.html',  context )



# def process_ajax_request():
#     template = ""
#     context = {}
#     category          =    request.POST.get('category')
#     selected_state    =    request.POST.get('selected_state')
#     fieldname         =    request.POST.get('fieldname')
#     # print "state", selected_state
#     if fieldname == "category":
#         sub_cat_list = SubCategories.objects.filter(category__title_slug = category)
#         context     =   {'sub_cat_list':sub_cat_list}
#         template    =  'fixit/main/main_snippet/subcategory_snippet.html'
#     elif fieldname  == "state":
#         areas_under_state = Area.objects.filter(state__state = selected_state)
#         context     =    {'areas_under_state': areas_under_state}
#         template    =    'fixit/main/main_snippet/areas_in_state_snippet.html'
#     return render(request, template, context )




# @login_required()
def createJobView(request):
    project_saved           =    False
    context                 =    {}
    context['states']       =    State.objects.all()
    #  process ajax request
    if request.is_ajax():
        template = ""
        context = {}
        category          =    request.POST.get('category')
        selected_state    =    request.POST.get('selected_state')
        fieldname         =    request.POST.get('fieldname')
        # print "state", selected_state
        if fieldname == "category":
            sub_cat_list = SubCategories.objects.filter(category__title_slug = category)
            context     =   {'sub_cat_list':sub_cat_list}
            template    =  'fixit/main/main_snippet/subcategory_snippet.html'
        elif fieldname  == "state":
            areas_under_state = Area.objects.filter(state__state = selected_state)
            context     =    {'areas_under_state': areas_under_state}
            template    =    'fixit/main/main_snippet/areas_in_state_snippet.html'
        return render(request, template, context )
        # process_ajax_request()

    if request.method       ==   "POST":
        uploadForm          =     JobUploadsForm(request.POST, request.FILES)
        email               =     request.POST.get('email')
        first_name          =     request.POST.get('fname')
        area                =     request.POST.get('lga')
        zone                =     get_zone(request.POST.get('state'), area)
        # print " zone caught in view: ", zone
        # check if email exists
        if not User.objects.filter(email =  email).exists():
            user_str = 'c' +  '-' + email +  '-' + first_name 
            return redirect(reverse('fixitCustomers:register-customer',kwargs={'source':'post-project', 'ref': user_str }))
        else:
            # Check if user is a tradesman or customer
            if not Customers.objects.filter(customer__email =  email).exists():
                user_str = 't' + '-' + email +  '-' + first_name  
                return redirect(reverse('fixitCustomers:register-customer', kwargs={'source':'post-project', 'ref': user_str }))

        postedby         =   Customers.objects.get(customer__email = email)
        ID               =   get_JobID(PostedJob)
        title            =   request.POST.get('job_title')
        category         =   JobCategories.objects.get(title_slug = request.POST.get('category'))
        startdate        =   request.POST.get('select_startdate')
        duration         =   request.POST.get('time_frame')
        description      =   request.POST.get('job_description')
        supplier         =   request.POST.get('supplier')
        zip_code         =   request.POST.get('zipcode')
        sub_category     =   SubCategories.objects.get(title_slug = request.POST.get('sub_category'))
        state            =   request.POST.get('state') # change this to state code
        lga              =   area 
        stage            =   request.POST.get('project_status')
        budget           =   request.POST.get('project_budget')
        
        new_Job  = PostedJob.objects.create(job_id=ID, job_category=category,job_sub_category=sub_category,
        job_title=title,description=description,start_date=startdate,postedby=postedby,location=state,
        area=lga,zip_code=zip_code,zone_id=zone,supplier=supplier,status='Open',views=0,time_frame=duration,
        budget=budget,current_stage=stage) 

        if uploadForm.is_valid():
            upload            =      uploadForm.save(commit = False)
            upload.zone       =      zone #change zone to use get_zone
            upload.job_id     =      ID
            upload.save()
            project_saved     =      True
        else:
            # print "No file uploaded"
            # set dummy picture here
            context['invalid_upload']  =  True

        context['project_saved']   =   True
        context['my_project']      =   new_Job
            
    # NOTIFY TRADESMEN IN THE POSTED CATEGORY WITH JOB DETAILS
    link  =   DOMAIN_PREFIX + category.title_slug + "/" + ID + "/" + slugify(title)
   
    message = '''Hello, <br/> A new project matching your area of specialization has just been 
    posted on''' + DOMAIN_PREFIX + '''. Click on the link below to view the details of this project and
    submit a quotation instantly. <br/><br/><br/> ''' + link + "<br/> <br/> Regards: <br/> The " + DOMAIN_PREFIX + "Team"
    #Send email to affected tradesmen

    notify_tradesmen(category, message) #UNCOMMENT WHEN DEPLOYING
    context['categories']          =      JobCategories.objects.all()
    context['uploads_form']        =      JobUploadsForm()
    return render(request,  'fixit/main/post-job.html',  context )

    




# @login_required()
def   catDetailsView(request):
    this_category = request.GET.get('category')
    ''' Populate jobs display by category page '''

    if JobCategories.objects.filter(title_slug = this_category).count() < 1:
        referer  =  request.META.get('HTTP_REFERER')
        return render(request, 'fixit/404.html', {'referer':referer } )

    pic_objs                  =    []
    response_objs             =    []
    response_lists            =    []
    proj_pix                  =    []
    response_count            =    []
    display_title             =    this_category.replace("-", " ")
    context                   =    {}
    subcategories             =    SubCategories.objects.filter(category__category_title = display_title)
    jobs_in_cat               =    PostedJob.objects.filter(job_category__category_title = display_title).order_by('-date_posted')

    #Check if there are jobs in this category
    if not jobs_in_cat.count() > 0:
        context['no_jobs'] = True
    responses  =  ""
    for job in jobs_in_cat:
        if JobUploads.objects.filter(job_id = job.job_id).exists():
            responses = Responses.objects.filter(job_id__job_id  =   job.job_id)
            pic_objs.append(JobUploads.objects.get(job_id  =   job.job_id))
            # response_count.append({responses:responses.count()})
        response_lists.append(responses)
        context['response_count'] = response_count
    for response in response_lists:
        # print "list length", len(response)
        response_count.append({response: len(response)})
        for obj in response:
            response_objs.append(obj)
    cat_list                  =    JobCategories.objects.all()
    cat_caption               =    JobCategories.objects.get(category_title = display_title).caption
    context['jobs_in_cat']    =    paginate_list(request, jobs_in_cat, 10)
    context['cat_list']       =    cat_list
    context['cat_title']      =    display_title
    context['cat_title_slug'] =    this_category
    context['cat_caption']    =    cat_caption
    context['subcategories']  =    subcategories
    context['uploads']        =    pic_objs
    context['zones']          =    Zone.objects.all()
    return render(request,  'fixit/main/category_details.html', context)






def jobsByZoneView(request, category, state, zone_id, zone):
    ''' Get jobs by zone classification '''
    context   =   {}
    if request.method == "POST":
        category = request.POST.get('inputed_category')
        # print 'Form category here', category
        context['category']     =     category.replace("-", " ")
        context['cate_slug']    =     category
        jobs_in_zone = PostedJob.objects.filter(zone_id = zone_id, job_category__title_slug = category, location = state).order_by('-date_posted')
    else:
        if  category  == "jobs":
            context['category']     = "All Categories"
            jobs_in_zone = PostedJob.objects.filter(zone_id = zone_id, location = state).order_by('-date_posted')
        else:
            jobs_in_zone = PostedJob.objects.filter(zone_id = zone_id, job_category__title_slug = category, location = state).order_by('-date_posted')
            context['category']     =     category.replace("-", " ")
            context['cate_slug']    =     category

        if jobs_in_zone.count() > 0:
            for job in jobs_in_zone:
                uploads  = JobUploads.objects.filter(zone = zone_id)
                # print 'All uploads', [upload for upload in uploads]
        else:
            uploads = ""
        if Zone.objects.filter(code = zone_id, state__state = state).exists():
            context['zone']     =     Zone.objects.get(code = zone_id, state__state = state)
    context['jobs']             =     paginate_list(request, jobs_in_zone, 10)
    context['categories']       =     JobCategories.objects.all() 
    context['uploads']          =     uploads
    context['zones']            =     Zone.objects.all()
    return render(request,  'fixit/main/jobs-by-zone.html', context)






def   jobDetailsView(request, category, id, title):
    ''' Display all fields to job owner but selected fields to public '''
    ''' compare job owner id to logged in user id and display appropriately '''
    context            =       {}
    responders         =       []
    category_title     =       category.replace("-"," ")
    category_slug      =       category    
    tradesmen_list     =       []
    tradesmen          =       []
    responses          =       get_Responses(id)

    if PostedJob.objects.filter(job_id=id).count() > 0:
        job = PostedJob.objects.get(job_id=id)
        views = job.views
        request.session['job_in_view'] = job.job_id
        PostedJob.objects.filter(job_id=id).update(views = views + 1)
    else:
        job  =  {}
        context['no_jobs_found']   =    True
    context['category_slug']       =    category_slug
    context['category_title']      =    category_title
    context['job']                 =    job
    context['job_title']           =    title.replace("-", " ")
    context['responses']           =    responses
    context['num_responses']       =    responses.count()

    # Get uploaded files for this job
    if JobUploads.objects.filter(job_id = id).exists():
        context['job_picture']         =    JobUploads.objects.get(job_id = id).picture
        context['job_document']        =    JobUploads.objects.get(job_id = id).document
    else:
        context['job_picture']         =    {}
        context['job_document']        =    {}

    for response in responses:
        responder   =   Tradesman.objects.filter(user__email = response.responder)
        responders.append(responder[0])
        print "responders", responder
    context['responders'] = responders
    
    return render(request,  'fixit/main/job_details.html', context)

    

    

def   contactView(request):
    return render(request,  'fixit/main/contact-us.html',  {} )

# def   FaqView(request):
#     return render(request,  'fixit/main/Faqs.html',  {} )

# def   TandCView(request):
#     return render(request,  'fixit/main/TandC.html',  {} )


# def   AboutView(request):
#     return render(request,  'fixit/main/about-us.html',  {} )





# class AboutView(TemplateView):
#     template_name = "fixit/main/about-us.html"




def   allJobsView(request):
    context                   =      {}    
    all_categories            =      JobCategories.objects.all()
    all_upload                =      JobUploads.objects.all()
    context['categories']     =      all_categories
    context['uploads']        =      all_upload
    context['zones']          =      Zone.objects.all()
    all_jobs                  =      PostedJob.objects.all().order_by('-date_posted')
    Jobs      =   paginate_list(request, all_jobs, 10)
    context['jobs']           =       Jobs
    responses = get_Responses("all")
    for response in responses:
        context['responses']  =  responses
    return render(request,  'fixit/main/all-jobs.html', context)







def   loginView(request):
    form = LoginForm()
    context = {}
    context['loginform']  =  form
    if request.method   ==  'POST':
        loginForm       =    LoginForm(data = request.POST)
        if loginForm.is_valid():
            email           =     request.POST.get('email').strip()
            password        =     request.POST.get('password').strip()
            auth_user       =     authenticate(email = email, password = password)
            auth_user       =     authenticate(username = email, password = password)
            if auth_user:
                user  =  auth_user
                if user.is_active:
                    login(request, auth_user) # log user in
                    request.session['logged_in'] = True

                    # #check login source page
                    if request.POST.get('next')  != "":
                        next  =   request.POST.get('next')
                        return redirect(next) #return to the called page

                    if user.groups.filter(name = 'Regular').exists():
                        return redirect(reverse('fixitCustomers:my-jobs'))
                    if user.groups.filter(name = 'Tradesman').exists():
                        # print "user is a tradesman.........."
                        return redirect(reverse('fixitTradesmen:tradesman-account'))

                        # return redirect(request.META['HTTP_REFERER' - 1])
                    # elif user.groups.filter(name = 'Administrators').exists():TO BE ACTIVATED LATER
                    #     return redirect(reverse('fixitAdmin:admin-dashboard'))    
                
                else:
                    messages.error(request, "This account has been deactivated. Please send a mail to activate@ndoozi.com.")
                    # context['inactive'] = True
                    return render(request,  'fixit/main/login.html', context)
            else:
                messages.error(request, "The login details you supplied are incorrect. Please check and try again.")
                # context['denied']   =  True
                return render(request,  'fixit/main/login.html', context)
        else:
            messages.error(request, "The login details you supplied are incorrect. Please check and try again.")
            # context['error']  = True
            return render(request,  'fixit/main/login.html', context)
    else:
        return render(request,  'fixit/main/login.html', context)






def logOutView(request):
    logout(request)
    return redirect(reverse('fixitMain:index'))



@ensure_csrf_cookie
def ajaxGetSubCat(request):
    if request.is_ajax():
        print request.POST.get('category')

    return render(request, 'fixitMain/main_snippet/subcategory_snippet.html', {})




def   blogView(request):
    return render(request,  'fixit/main/blog.html',  {} )


def   careerView(request):
    return render(request,  'fixit/main/career.html',  {} )
