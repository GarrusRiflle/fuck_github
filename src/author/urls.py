from django.conf.urls import include, url, patterns
from django.contrib import admin

from question.views import UserQuestionsListView

admin.autodiscover()

urlpatterns = [
    url(r'^login/$', 'author.views.login'),
    url(r'^logout/$', 'author.views.logout'),
    url(r'^register/$', 'author.views.register'),

    url(r'^questions/$', UserQuestionsListView.as_view(), name='user-questions-view'),
    url(r'^answers/$', 'author.views.answers'),
    url(r'^settings/$', 'author.views.settings'),
]