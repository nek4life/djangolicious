from django.db import models
from tagging.fields import TagField

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
    objects           = models.Manager()
    published_objects = PublicManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('-save_date',)
        
    def save(self, **kwargs):
        if not self.slug:
            from django.template.defaultfilters import slugify
            self.slug = slugify(self.title)
        super(Bookmark, self).save(force_insert=False)