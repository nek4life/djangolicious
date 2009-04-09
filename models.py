from django.db import models
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from pydelicious import DeliciousAPI
import datetime

from djangolicious.managers import PublicManager

class Bookmark(models.Model):
    title             = models.CharField(max_length=250)
    slug              = models.SlugField()
    url               = models.URLField(unique=True)
    tags              = TagField()
    notes             = models.TextField()
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
        ordering = ('-save_date',)
        
    def save(self, syncAPI=False):
        if not self.slug:
            self.slug = slugify(self.title)
        if not syncAPI:
            self.queued = True
            if not self.id:
                self.save_date =  datetime.datetime.now()
                                     
        super(Bookmark, self).save(force_insert=False)