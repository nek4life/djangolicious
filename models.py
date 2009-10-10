import datetime
# Django imports
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
# Comment Moderation Imports
from django.conf import settings
from django.contrib.comments.moderation import CommentModerator, moderator
from django.utils.encoding import smart_str
# Dependancy Imports
from akismet import Akismet
from tagging.fields import TagField
from smartypants import smartyPants
from markdown import markdown
# Djangolicious Imports
from djangolicious.managers import PublicManager

class Bookmark(models.Model):
    """ Bookmark model """
    title             = models.CharField(max_length=250)
    slug              = models.SlugField(max_length=250)
    url               = models.URLField(max_length=250, unique=True, verify_exists=False)
    tags              = TagField()
    notes             = models.TextField(blank=True, null=True)
    notes_html        = models.TextField(blank=True)
    post_hash         = models.CharField(max_length=100)
    post_meta         = models.CharField(max_length=100)
    save_date         = models.DateTimeField(default=datetime.datetime.now)
    shared            = models.BooleanField(default=True)
    featured          = models.BooleanField(default=False)
    queued            = models.BooleanField(default=False)
    enable_comments   = models.BooleanField(default=True)
    objects           = models.Manager()
    shared_objects    = PublicManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('-save_date',)
        
    def save(self, syncAPI=False, *args, **kwargs):
        """
        syncAPI is True for all calls from djangolicious.utils.DeliciousSyncDB.
        
        This allows for a check to see if a bookmark has been created locally 
        or remotely through the syncAPI.
        
        Bookmarks that have been flagged as queued are processed by the
        DeliciousSyncDB.processQueue sending locally modified bookmarks
        back to Delicious.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        if self.notes:
            self.notes_html  = smartyPants(markdown(self.notes))
        if not syncAPI:
            self.queued=True                           
        super(Bookmark, self).save(**kwargs)
        
    @permalink
    def get_absolute_url(self):
        return ('bookmark_detail', None, {
            'year': self.save_date.year,
            'month': self.save_date.strftime('%b').lower(),
            'day': self.save_date.day,
            'slug': self.slug
        })
        
           
class BookmarkModerator(CommentModerator):
    auto_moderate_field = 'save_date'
    enable_field = 'enable_comments'
    moderate_after = 30
    email_notification = True
    
    def moderate(self, comment, content_object, request):
        already_moderated = super(PostModerator,
            self).moderate(comment, content_object, request)
        if already_moderated:
            return True
        akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                                blog_url="http://%s/" %
                                Site.objects.get_current().domain)
        if akismet_api.verify_key():
            akismet_data = { 'comment_type': 'comment',
                                'referrer': request.META['HTTP_REFERER'],
                                'user_ip': comment.ip_address,
                                'user_agent': request.META['HTTP_USER_AGENT'] }
            return akismet_api.comment_check(smart_str(comment.comment),
                                            akismet_data,
                                            build_data=True)
        return False
        
moderator.register(Bookmark, BookmarkModerator)