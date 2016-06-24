from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from fixitTradesmen import views

from fixitTradesmen import views



# Create your urls here.
urlpatterns = [
        # url(r'^tradesman/register/source=(?P<source>[-\w]+)$', views.RegisterTradesmanView.as_view(),  name='register-tradesman'),
        url(r'^tradesman/register/source=(?P<source>[-\w]+)$', views.RegisterTradesmanView,  name='register-tradesman'),
        # url(r'^tradesman/dashboard/$', views.tradesmanAccountView,  name='tradesman-account'),
        url(r'^professional/profile/$', views.tradesmanAccountView,  name='tradesman-account'),

        url(r'^tradesman/profile/Id=(?P<user_id>[-\w]+)/$', views.tradesmanProfileView,  name='profile'),

        url(r'^tradesman/verification/$', views.tradesmanVerifyView,  name='verify-tradesman'),

        url(r'^respond/(?P<pid>[-\d]+)/(?P<title>[-\w]+)/(?P<action>[-\w]+)$', views.jobResponseView,  name='respond_to_job'),

        url(r'^Response/save-response/$', views.saveJobResponse,  name='save-response'),

        url(r'^how-it-works/$',  views.howItWorksView, name="how-it-works"),
        url(r'^pricing/$', views.pricingView, name="pricing"),
] 

# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

##                       url(r'^login/$', 'Client_Login', name='client_login'),
##                       
##
##                       )
