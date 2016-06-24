from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from fixitMain import views


from django.views.generic import TemplateView



# Create your urls here.
urlpatterns = [
             url(r'^$',  views.mainIndexView,    name='index'),
             url(r'^project/new/create/category=(?P<category>[-\w]+)$', views.displayJobForm,  name='postjob'),
             url(r'^project/new/create/$', views.createJobView,  name='createjob'),
             url(r'^general/contact-us/$', views.contactView,  name='contact-us'),
             url(r'^general/Frequently-Asked-Questions/$', TemplateView.as_view(template_name = "fixit/main/Faqs.html"),  name='FAQs'),
             url(r'^legal/Terms-and-Conditions/$', TemplateView.as_view(template_name = "fixit/main/TandC.html"),  name='TandC'),
             url(r'^general/about-us/$', TemplateView.as_view(template_name = "fixit/main/about-us.html"),  name='about-us'),
             url(r'^general/all-jobs/$', views.allJobsView,  name='all-jobs'),
             url(r'^jobs/$', views.catDetailsView,  name='cat_details'),
             url(r'^(?P<category>[-\w]+)/(?P<id>[-\d]+)/(?P<title>[-\w]+)/$', views.jobDetailsView,  name='job_details'),
             url(r'^(?P<category>[-\w]+)/(?P<state>[-\w]+)/(?P<zone_id>[-\w]+)/(?P<zone>[-\w]+)/$', views.jobsByZoneView,  name='job_by_zones'),
             url(r'^accounts/login/$', views.loginView,  name='login'),
             url(r'^accounts/logout/$', views.logOutView,  name='logout'),
             url(r'^content/blog/$', views.blogView,  name='blog'),
             url(r'^content/careers/$', views.careerView,  name='careers'),
             url(r'^project/new/create/$', views.ajaxGetSubCat,  name='populate_subcategory'),

             url(r'^thank-you/(?P<userID>[-\w]+)/$',   views.signupSuccess,  name='signup_success'),
             # url(r'^thank-you/(?P<useremail>[-\w@\d\.]+)$',   views.signupSuccess,  name='signup_success'),

                ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


 