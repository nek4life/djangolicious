from django.contrib import admin
from djangolicious.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('title',) }

admin.site.register(Bookmark, BookmarkAdmin)