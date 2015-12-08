from django.conf.urls import include, url, patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^(?P<question_id>\d+)/$', 'question.views.question'),
    url(r'^addrate/(?P<question_id>\d+)/$', 'question.views.addrate'),
    url(r'^cutrate/(?P<question_id>\d+)/$', 'question.views.cutrate'),
    url(r'^addcomment/(?P<question_id>\d+)/$', 'question.views.addcomment'),
    url(r'^add/$', 'question.views.addquestion'),

    url(r'^like/$', 'question.views.like', name='like'),
]