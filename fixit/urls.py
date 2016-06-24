from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'fixit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',               include(admin.site.urls)),
    url(r'^',                     include('fixitMain.urls',               namespace    =     'fixitMain')),
    url(r'^administrator',        include('fixitAdmin.urls',              namespace    =     'fixitAdmin')),
    url(r'^',                     include('fixitCustomers.urls',          namespace    =     'fixitCustomers')),
    url(r'^',                     include('fixitTradesmen.urls',          namespace    =     'fixitTradesmen')),
                       
]
