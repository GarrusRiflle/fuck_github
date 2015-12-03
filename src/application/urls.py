from django.conf.urls import include, url
from django.contrib import admin
from question import urls
from author import urls
from question.views import NewQuestionsListView, TopQuestionsListView, TagQuestionsListView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^new/$', NewQuestionsListView.as_view(), name='new-questions-view'),
    #url(r'^top/$', TopQuestionsListView.as_view(), name='top-questions-view'),
    url(r'^new/$', 'question.views.new_questions'),
    url(r'^top/$', 'question.views.top_questions'),
    url(r'^tag/(?P<slug>[-\w]+)/$', TagQuestionsListView.as_view(), name='tagged'),

    url(r'^question/', include('question.urls')),
    url(r'^auth/', include('author.urls')),
]
