from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from fixitCustomers import views


# Create your urls here.
urlpatterns  =  [
             
	url(r'^accounts/create/source=(?P<source>[-\w]+)/ref=(?P<ref>[-\w@\d\.]+)$', views.custRegForm,  name='register-customer'),
	url(r'^accounts/create/$', views.custSignUp,  name='sign-up-customer'),
	url(r'^accounts/resetpassword/$', views.resetPasswordView,  name='reset-pw'),
	url(r'^accounts/jobs/$', views.custMyjobsView,  name='my-jobs'),
	url(r'^accounts/job/close/Id=(?P<job_id>[-\w]+)$', views.rate_Close_JobView,  name='close-job'),
	url(r'^accounts/profile/$', views.custAccountView,  name='my-account'),
	url(r'^jobs/edit/Id=(?P<job_id>[-\w]+)$', views.jobEditView,  name='edit-job'),
	url(r'^accept_tradesman/(?P<job_id>[-\d]+)/(?P<tradesman>[-\w]+)$', views.acceptTradesmanView,  name='accept-tradesman'),
	url(r'^jobs/Id=(?P<job_id>[-\w]+)$', views.custJobDetailView,  name='job_details'),
	url(r'^message/for=(?P<job_id>[-\w]+)$', views.sendMessageView,  name='send-message'),
	url(r'^profile/edit/$', views.editProfileView,  name='edit-profile'),
]


