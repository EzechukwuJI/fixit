from django.db import models
from django.contrib.auth.models import User
# from fixitMain.models import User 
from django.template.defaultfilters import slugify
import datetime

# from fixitMain.callables import get_UserID





# Create your models here.


class Customers(models.Model):
	userID                  =           models.CharField("Customer ID", max_length = 6)
	customer                =           models.OneToOneField(User)
	address             	=           models.CharField('Contact Adress', max_length = 125)
	city                	=           models.CharField(max_length = 50)
	area                	=           models.CharField(max_length = 50) 
	state               	=           models.CharField(max_length = 50)
	country             	=           models.CharField(max_length = 50)
	phone_no            	=           models.CharField(max_length = 50)
	account_type            =           models.CharField(max_length = 50)
	reg_code                =           models.CharField(max_length = 50)
	          


	def __unicode__(self):
		return '%s' %(self.customer.username)


	def save(self, *args, **kwargs):
		self.account_type  =   "Regular"
		# self.custID        =   get_UserID('Customer')
		super(Customers, self).save(*args, **kwargs) 


