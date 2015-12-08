from django.conf.urls import include, url
from django.contrib import admin

from question.views import TagQuestionsListView, NewQuestionsListView, TopQuestionsListView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^new/$', NewQuestionsListView.as_view(), name='new-questions-view'),
    url(r'^top/$', TopQuestionsListView.as_view(), name='top-questions-view'),
    url(r'^tag/(?P<slug>[-\w]+)/$', TagQuestionsListView.as_view(), name='tag-questions-view'),
    url(r'^(?P<username>\w+)/$', 'author.views.profile'),

    url(r'^question/', include('question.urls')),
    url(r'^profile/', include('author.urls')),

    url(r'^search/', include('haystack.urls', app_name='search', namespace='search')),
]
