from django.conf.urls import patterns, url
##from django.contrib import admin
from fixitAdmin import views




# Create your views here.
urlpatterns = [
                       url(r'^$',  views.index, name='index'),

                       ]
