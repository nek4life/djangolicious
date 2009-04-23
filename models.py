from django.db import models
from django.template.defaultfilters import slugify
from tagging.fields import TagField
import datetime
from smartypants import smartyPants
from markdown import markdown

from djangolicious.managers import PublicManager

class Bookmark(models.Model):
    """ Bookmark model """
    title             = models.CharField(max_length=250)
    slug              = models.SlugField(max_length=250)
    url               = models.URLField(unique=True)
    tags              = TagField()
    notes             = models.TextField(blank=True, null=True)
    notes_html        = models.TextField(blank=True)
    post_hash         = models.CharField(max_length=100)
    post_meta         = models.CharField(max_length=100)
    save_date         = models.DateTimeField()
    shared            = models.BooleanField(default=True)
    queued            = models.BooleanField(default=False)
    objects           = models.Manager()
    published_objects = PublicManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('save_date',)
        
    def save(self, syncAPI=False, **kwargs):
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
        if not syncAPI:
            self.queued = True
            if not self.id:
                self.save_date =  datetime.datetime.now()
            if self.notes:
                self.notes_html  = smartyPants(markdown(self.notes))                                     
        super(Bookmark, self).save(force_insert=False)