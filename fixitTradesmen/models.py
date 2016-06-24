from django.db import models
from django.contrib.auth.models import User 
from fixitMain.models import Country, State, Zone, Area
from django.template.defaultfilters import slugify
import datetime


from fixitMain.models import  SubCategories, PostedJob
from fixitMain.models import  JobCategories 

# Create your models here.

class Biodata(models.Model):
	tradesman    			=     		models.OneToOneField(User)
	userID        		    =  			models.CharField("Tradesman ID", max_length = 6)
	address             	=           models.CharField('Contact Adress', max_length = 125)
	city                	=           models.CharField(max_length = 50)
	zone                	=           models.CharField(max_length = 50) 
	state               	=           models.CharField(max_length = 50)
	country             	=           models.CharField(max_length = 50)
	phone_no            	=           models.CharField(max_length = 50)
	account_type            =           models.CharField(max_length = 50)
	passport                =           models.ImageField ('Tradesman passport', upload_to = 'Tradesmen passports', blank=True, null=True)
	

	def __unicode__(self):
		return '%s' %(self.tradesman.username)

	def save(self, *args, **kwargs):
		self.account_type  = "tradesman"
		super(Biodata, self).save(*args, **kwargs)  
		




class  CoporateData(models.Model):
	user                    =           models.OneToOneField   (Biodata, verbose_name = 'For ')
	logo                    =           models.ImageField      ('Coporate Logo', upload_to = 'Tradesmen_Logo')
	verification_code       =           models.CharField       ('verification_colour', max_length = 11)
	rating                  =           models.CharField       ('Agregate Rating', max_length = 5)
	jobs_count              =           models.CharField       ('Total jobs executed', max_length = 6)
	is_verified             =           models.BooleanField    (default = False)
	subscription_type       =           models.CharField       (max_length  = 25)
	category                =           models.ForeignKey      (JobCategories, verbose_name = 'Job specialization')
	sub_category            =           models.ForeignKey      (SubCategories, verbose_name = 'Sub specialization')
	sales_pitch             =           models.TextField       (max_length = 300, help_text ='Briefly describe what you do')
	company_name            =           models.CharField       (max_length  = 75)
	name_slug               =           models.SlugField       (max_length = 100)

	
	def save(self, *args, **kwargs):
		self.name_slug  = slugify(self.company_name)
		super(CoporateData, self).save(*args, **kwargs)   

	def __unicode__(self):
		return '%s' %(self.company_name) 


SUBSCRIPTION_TYPE = (
	('Regular', 'Regular'),
	('PAYE', 'PAYE'),
	)



class Tradesman(models.Model):
	
	user   			        =     		models.OneToOneField(User)
	# coporate info
	userID        		    =  			models.CharField("Tradesman ID", max_length = 6)
	company_name            =           models.CharField       (max_length  = 75, blank=True)
	company_name_slug       =           models.SlugField       (max_length = 100)
	sales_pitch             =           models.TextField       (max_length = 300, help_text ='Briefly describe what you do')
	company_logo            =           models.ImageField      ('Coporate Logo', upload_to = 'Tradesmen_Logo', null=True, blank = True)
	subscription_type       =           models.CharField       (max_length  = 15, choices = SUBSCRIPTION_TYPE)
	category                =           models.ForeignKey      (JobCategories, verbose_name = 'Job specialization')
	sub_category            =           models.ForeignKey      (SubCategories, verbose_name = 'Sub specialization')

	is_verified             =           models.BooleanField    (default = False)
	verification_code       =           models.CharField       ('verification_colour', max_length = 11)
	rating                  =           models.CharField       ('Aggregate Rating', max_length = 5, default = 0)
	jobs_count              =           models.CharField       ('Total jobs executed', max_length = 6, default = 0)

	#  Location
	address             	=           models.CharField('Contact Adress', max_length = 125)
	city                	=           models.CharField(max_length = 50)
	zone                	=           models.CharField(max_length = 50) 
	LGA                 	=           models.CharField(max_length = 50) 
	state               	=           models.CharField(max_length = 50)
	country             	=           models.CharField(max_length = 50)
	phone_no            	=           models.CharField(max_length = 50)
	passport                =           models.ImageField ('Tradesman passport', upload_to = 'T-passports', blank=True, null=True)
	
	#  document uploads
	licence                 =       	models.ImageField (upload_to = 'T-Documents',   null = True, blank = True,  help_text = "Drivers licence or international passport")
	bank_slip               =       	models.ImageField (upload_to = 'T-Documents',   null = True, blank = True,  help_text = "For name reconciliation purposes only")
	utility_bill            =       	models.FileField  (upload_to = 'T-Documents',   null = True, blank = True,  help_text = "For address reconciliation purposes only")
	certificate             =       	models.FileField  (upload_to = 'T-Documents',   null = True, blank = True,  help_text = "For address reconciliation purposes only")


	def __unicode__(self):
		return '%s' %(self.user.username)

	def save(self, *args, **kwargs):
		self.subscription_type  = "Regular"
		self.company_name_slug = slugify(self.company_name)
		super(Tradesman, self).save(*args, **kwargs)  












class Documents(models.Model):
	user     		    	=		models.OneToOneField(Tradesman, verbose_name = 'For ')
	licence                 =       models.ImageField ('Authorized Identity', max_length = 125, 
													help_text = "Drivers licence or international passport")
	bank_slip               =       models.ImageField ('Bank slip', max_length = 125, null = True, blank = True,
													help_text = "For name reconciliation purposes only")
	utility_bill            =       models.FileField (max_length = 125, null = True, blank = True,
													help_text = "For address reconciliation purposes only")
	certificate             =       models.FileField(max_length = 125, null = True, blank = True,
													help_text = "For address reconciliation purposes only")

	def __unicode__(self):
		return self.user.user_id





class JobList(models.Model):
	tradesman             =    models.ForeignKey    (Tradesman, verbose_name = "Job Executed by")
	job                   =    models.ForeignKey    (PostedJob, verbose_name =    "Job responded to")  
	date_closed           =    models.DateTimeField (auto_now = False, auto_now_add = True) 
	rating                =    models.CharField     (max_length = 4, verbose_name = "Customer rating for this job", default = 0) 
	date_added            =    models.DateTimeField (auto_now = False, auto_now_add = True)
	status                =    models.CharField     (max_length = 15)
	fee                   =    models.CharField     (max_length = 10)
	review                =    models.TextField     (max_length = 300, null = True, blank = True)

	def __unicode__(self):
		return '%s %s' %(self.job.job_id, self.status)


