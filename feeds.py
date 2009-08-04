from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from djangolicious.models import Bookmark

current_site = Site.objects.get_current()

class LatestBookmarksFeed(Feed):
    copyright = "http://%s/about/copyright/" % current_site.domain
    description = "Latest Links on %s" % current_site.name
    feed_type = Atom1Feed
    item_copyright = "http://%s/about/copyright/" % current_site.domain
    link = "/feeds/links/"
    title = "%s: Latest Links" % current_site.name
    
    def items(self):
        return Bookmark.shared_objects.all()[:15]
        
    def item_pubdate(self, item):
        return item.save_date
        
    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain,
                                 item.save_date.strftime('%Y-%m-%d'),
                                 item.get_absolute_url())