from django.conf.urls.defaults import *
from djangolicious import views

urlpatterns = patterns('djangolicious.views',

    url(r'^$',
        view=views.bookmark_list,
        name='bookmark_list'),
    
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
        view=views.bookmark_detail,
        name='bookmark_detail'),

   url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
        view=views.bookmark_archive_day,
        name='bookmark_archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        view=views.bookmark_archive_month,
        name='bookmark_archive_month'),

    url(r'^(?P<year>\d{4})/$',
        view=views.bookmark_archive_year,
        name='bookmark_archive_year'),

    url(r'^tags/(?P<tag>[^/]+)/$',
        view=views.bookmark_tag_detail,
        name='bookmark_tag_detail'),
)