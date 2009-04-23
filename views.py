from django.shortcuts import render_to_response
from django.views.generic import list_detail, date_based
from djangolicious.models import Bookmark
from tagging.views import tagged_object_list

def bookmark_list(request, page=0):
    return list_detail.object_list(
        request,
        queryset = Bookmark.published_objects.all(),
        template_object_name = 'bookmark',
        page = page,
        paginate_by = 10,
    )
    
def bookmark_detail(request, slug, year, month, day):
    return date_based.object_detail(
        request,
        slug = slug,
        year = year,
        month = month,
        day = day,
        date_field = 'published',
        template_object_name = 'bookmark',
        queryset = Bookmark.published_objects.all(),
    )
    
def bookmark_archive_day(request, year, month, day):
    return date_based.archive_day(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'published',
        template_object_name = 'bookmark',
        queryset = Bookmark.published_objects.all(),
    )
    
def bookmark_archive_month(request, year, month):
    return date_based.archive_month(
        request,
        year = year,
        month = month,
        date_field = 'published',
        template_object_name = 'bookmark',
        queryset = Bookmark.published_objects.all(),
    )
    
def bookmark_archive_year(request, year):
    return date_based.archive_year(
        request,
        year = year,
        date_field = 'published',
        template_object_name = 'bookmark',
        queryset = Bookmark.published_objects.all(),
        make_object_list = True,
    )
    
def bookmark_tag_detail(request, tag):
    queryset = Bookmark.published_objects.all()
    return tagged_object_list(
        request,
        queryset,
        tag,
        paginate_by=10,
        allow_empty=True,
        template_object_name='bookmark',
        template_name='djangolicious/bookmark_list.html')