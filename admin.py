from django.contrib import admin
from djangolicious.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('title',) }
    exclude = ('post_hash', 'post_meta', 'save_date', 'queued', 'notes_html')

admin.site.register(Bookmark, BookmarkAdmin)