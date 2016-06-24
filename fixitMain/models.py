from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 



from fixitCustomers.models import Customers
# from fixitTradesmen.models import CoporateData as Tradesman

##from fixitMain.callables import get_catID
# Create your models here.



# class User(User):
#     account_type    =    models.CharField(max_length = 15)


# Job categories
class JobCategories(models.Model):
    caption             =    models.CharField(max_length = 300, help_text = "A descriptive note about he category in view")
    category_title      =    models.CharField(max_length = 150)
    title_slug          =    models.SlugField(unique=True,  max_length = 100)


    def save(self, *args, **kwargs):
        self.title_slug  = slugify(self.category_title)
        super(JobCategories, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.category_title



class SubCategories(models.Model):
    caption              =    models.CharField(max_length = 300, help_text = "A descriptive note about the subcategory in view")
    subcategory_title    =    models.CharField("Sub Category",  max_length = 150)
    category             =    models.ForeignKey(JobCategories, related_name = "subcategories", verbose_name = "Category", on_delete = models.CASCADE)
    title_slug           =    models.SlugField(unique=True, max_length = 100)


    def save(self, *args, **kwargs):
        self.title_slug  = slugify(self.subcategory_title)
        super(SubCategories, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.subcategory_title


class PostedJob(models.Model):
    job_id               =     models.CharField(max_length = 10, unique =  True)
    job_category         =     models.ForeignKey(JobCategories, verbose_name = 'Category')
    job_sub_category     =     models.ForeignKey(SubCategories, verbose_name = 'Sub Category')
    job_title            =     models.CharField('Job title',    max_length = 100)
    description          =     models.CharField('Description', max_length = 300)
    start_date           =     models.CharField('Expected start date', max_length = 20)
    date_posted          =     models.DateTimeField(auto_now = False, auto_now_add = True)
    postedby             =     models.ForeignKey(Customers, verbose_name="Requested by")
    location             =     models.CharField(max_length = 75)
    area                 =     models.CharField(max_length = 75)
    zip_code             =     models.IntegerField()
    zone_id              =     models.CharField(max_length  =  10)
    supplier             =     models.CharField('Materials supplied by:', max_length = 20)
    status               =     models.CharField(max_length = 15)
    views                =     models.IntegerField('Views', default = 0)
    title_slug           =     models.SlugField(max_length = 110)
    time_frame           =     models.CharField(max_length = 75)
    budget               =     models.CharField(max_length = 75)
    current_stage        =     models.CharField(max_length = 75)
    num_response         =     models.IntegerField(default=0)
    taken_by             =     models.CharField(max_length = 125, default = "")
    review               =     models.TextField(max_length = 300, null = True, blank = True)
    edited_on            =     models.DateTimeField(auto_now = False, auto_now_add = True)

    def save(self, *args, **kwargs):
        self.title_slug  = slugify(self.job_title)
        super(PostedJob, self).save(*args, **kwargs)


    def __unicode__(self):
        return '%s' %(self.job_title)


class Responses(models.Model):
    ''' Display all fields to job owner but selected fields to public '''

    job_id               =       models.ForeignKey  (PostedJob, verbose_name = 'Related To')
    responder            =       models.CharField   ('Tradesman', max_length = 12) #fed with info from hidden form with tradesman ID
    response_note        =       models.CharField   ('Comment from Tradesman', max_length = 300)
    quoted_amount        =       models.CharField   (max_length = 10) 
    date_posted          =       models.DateTimeField ( auto_now = False, auto_now_add = True)
    supply_estimate      =       models.CharField    ('Estimated amount for materials', 
                                        help_text = 'Estimated amount for materials', max_length = 15)
    supply_list          =       models.CharField('List of materials',max_length = 500, 
                                        help_text = 'optionally list the needed materials')

    def __unicode__(self):
        return '%s %s' %(self.job_id.job_title, self.responder)


class Country(models.Model):
    code             =      models.IntegerField()
    country          =      models.CharField(max_length  =  50)
    longitude        =      models.CharField(max_length = 20)
    latitude         =      models.CharField(max_length = 20)

    def __unicode__(self):
        return self.country

class State(models.Model):
    code            =    models.IntegerField()
    state           =    models.CharField(max_length  =  75)
    longitude       =    models.CharField(max_length = 20)
    latitude        =    models.CharField(max_length = 20)
    country         =    models.ForeignKey(Country, verbose_name  =  "Country")

    def __unicode__(self):
        return  '%s' %(self.state)


class  Zone(models.Model):
    code         =       models.CharField(max_length = 7)
    name         =       models.CharField(max_length  =   75)
    state        =       models.ForeignKey(State, verbose_name  =   "State")

    def __unicode__(self):
        return  '%s %s' %(self.name, self.state.state)




    def __unicode__(self):
        return  '%s' %(self.name)

class  Area(models.Model):
    code            =    models.CharField(max_length = 7)
    name            =    models.CharField(max_length = 75)
    longitude       =    models.CharField(max_length = 20)
    latitude        =    models.CharField(max_length = 20)
    zone            =    models.ForeignKey(Zone, verbose_name  =   "Zone")
    state           =    models.ForeignKey(State, verbose_name  =   "State")

    def __unicode__(self):
        return self.name


class JobUploads(models.Model):
    zone                  =     models.CharField(max_length  =  10)
    job_id                =     models.CharField(max_length  =  11)
    date_uploaded         =     models.DateTimeField('Date uploaded', auto_now = False, auto_now_add = True)
    picture               =     models.ImageField(upload_to = 'job_images', max_length = 125, null=True, blank=True)
    document              =     models.FileField(upload_to = 'job_documents', max_length = 125, null=True, blank=True)

    def __unicode__(self):
        return '%s %s' %(self.job_id, self.picture)






class Messages(models.Model):
    sent_from            =    models.ForeignKey(User, verbose_name = "sender")
    # sent_to              =    models.CharField("receiver", max_length = 25)
    datetime_sent        =    models.DateTimeField(auto_now = False, auto_now_add = True)
    related_job          =    models.ForeignKey(PostedJob)
    message              =    models.TextField()
        

    def __unicode__(self):
        return self.message

