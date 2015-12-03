from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^login/$', 'author.views.login'),
    url(r'^logout/$', 'author.views.logout'),
    url(r'^register/$', 'author.views.register'),
]
