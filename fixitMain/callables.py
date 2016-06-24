import string
import random
import datetime
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, EmailMultiAlternatives


from fixitMain.models import Responses, Zone, Area, Messages
from fixitMain.models import PostedJob as new_project, JobUploads as uploads, State, Area, SubCategories, JobCategories
from fixitTradesmen.models import CoporateData as CD, JobList
from fixitCustomers.models import Customers


def get_catID(model):
    ID = str(random.randrange(1234, 9999)) 
    if model.objects.filter(cat_Id = ID).count > 0:
        ID = str(random.randrange(1234, 9999)) 
    return ID



def get_JobID(model):
    ID =  str(random.randrange(11, 99)) + str(datetime.date.today())[2:].replace("-", "") + str(random.randrange(11, 99))
    if model.objects.filter(job_id = ID).exists():
        ID = str(random.randrange(10, 99)) + str(datetime.date.today())[2:].replace("-", "") + str(random.randrange(11, 99))
    return ID 


def get_UserID(model):
    ID =  str(random.randrange(0, 9)) + str(random.randrange(10, 99)) + str(random.randrange(10, int(str(datetime.date.today())[2:].split("-")[0])))
    if model.objects.filter(userID = ID).exists():
        get_userID(model)
        # ID = str(random.randrange(0, 9)) + str(random.randrange(10, 99)) + str(random.randrange(10, int(str(datetime.date.today())[2:].split("-")[0])))
    return ID
    
    



def get_Responses(job_id):
    if job_id == "all":
        return Responses.objects.all()
    else:
        return Responses.objects.filter(job_id__job_id = job_id)




def rateJobPerformance(score_list):
    final_score = 0
    for score in score_list:
        final_score += float(score)/5
    return  int(final_score)





def get_TradesmanRating(tradesman_email):
    ratings = [t.rating for t in JobList.objects.filter(tradesman__user__email = tradesman_email, status = "Closed")]
    aggregate = 0
    for score in ratings:
        aggregate  += float(score)
    aggregate  /=   len(ratings)
    # print "aggregate ", aggregate
    return round(aggregate, 0)


def DisplayRating(tradesman_email):
    ratings              =    [t.rating for t in JobList.objects.filter(tradesman__user__email = tradesman_email, status = "Closed")]
    score                =    {}
    score_count_list     =    []
    for value in ratings:
        score[value] = ratings.count(value)
    score_count_list.append(score)
    print "score list : ", score_count_list
    return score_count_list


def paginate_list(request, objects_list, num_per_page):
    paginator   =   Paginator(objects_list, num_per_page) # show number of jobs per page
    page  = request.GET.get('page')
    try:
        paginated_list  = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        paginated_list   =   paginator.page(1)
    except  EmptyPage:
        #if page is out of range(e.g 9999), deliver last page of results
        paginated_list      =   paginator.page(paginator.num_pages)
    return paginated_list



def get_zone(state, area):
    zones_in_state  =  Zone.objects.filter(state__state   =   state)
    for zone in zones_in_state:
        Areas = Area.objects.filter(zone__code = zone.code)  # Try using area code in place of 'name'
        for location in Areas:
            # print "location name lower: ", location.name.lower()
            if location.name.lower() ==  area.lower():
                return zone.code
            else:
                return 'zn00' # zone code for others (Unmatched zones)


def pGen():
    random_chars = "".join([random.choice(string.ascii_letters + string.digits + string.punctuation[3:7]) for n in range(8)])
    return random_chars


       

def notify_tradesmen(category, html_message):
    notify = ""
    tradesmen_email_list    = [ person.user.tradesman.email for person in CD.objects.filter(category = category, is_verified = True)]
    if tradesmen_email_list  != []:
        subject                  =      'New job notification'
        content                  =       html_message
        sender                   =      'notifications@ndoozi.com'
        recipient_list           =       tradesmen_email_list
        headers                  =       {}
        notify  = EmailMessage(subject = subject, body = content, 
            from_email = sender, bcc = recipient_list)
        notify.content_subtype = "html" # leaves main type as text/html
        notify.send(fail_silently = False)
        # print 'Recipients: ', notify.recipients()
        return notify.recipients()
    else:
        print 'No recipient selected'
    return 




def retrieveMessages(job_id, job_owner):
   messages =  Messages.objects.filter(related_job__job_id = job_id, 
        related_job__postedby__customer__email = job_owner).order_by('datetime_sent')
   return messages

 
def processAjaxRequest(request):
    if request.is_ajax():
        template = ""
        context = {}
        category          =    request.POST.get('category')
        selected_state    =    request.POST.get('state')
        fieldname         =    request.POST.get('fieldname')
        if fieldname == "category":
            sub_cat_list = SubCategories.objects.filter(category__title_slug = category)
            context     =   {'sub_cat_list':sub_cat_list}
            template    =  'fixit/main/main_snippet/subcategory_snippet.html'
        elif fieldname  == "state":
            areas_under_state = Area.objects.filter(state__state = selected_state)
            context     =    {'areas_under_state': areas_under_state}
            template    =    'fixit/main/main_snippet/areas_in_state__snippet.html'
        return render(request, template, context )



def get_content_tuple(Objectmodel, **kwargs):
    content_tuple = ()
    if Objectmodel == JobCategories:
        for item in Objectmodel.objects.all():
            item_tuple = ((item.title_slug, item.category_title),) 
            content_tuple += item_tuple
    else:
        pass
    return content_tuple


# class Registration_code():

#     def generate_reg_code(self):
#         tr_code = ""
#         alpha = "abcdefghjklmnpqrstuvwxyz"
#         for counter in range(5):
#             tr_code += random.choice(alpha.upper())
#             tr_code += random.choice(alpha)
#             tr_code += str(random.randrange(1,9))
#             tr_code += random.choice(alpha.upper()[::-1])
#         return tr_code


#     def get_unique_code(self, referenced_object_model):
#         reg_id = self.generate_reg_code()
#         if referenced_object_model.objects.filter(reg_code = reg_id).exists(): # ensure unique reference number
#             self.get_unique_code()
#         return reg_id







