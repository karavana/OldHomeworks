from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^create/$', 'main.views.createview'),
	url(r'^login/$', 'main.views.loginview'),
	url(r'^logout/$', 'main.views.logoutview'),
	url(r'^places/$', 'main.views.places'),
	url(r'^events/$', 'main.views.events'),
	url(r'^$', 'main.views.home'),
	url(r'^show/$', 'main.views.show'),

)
