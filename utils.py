from pydelicious import DeliciousAPI
import dateutil.parser, dateutil.tz

from djangolicious.models import Bookmark

class DeliciousSyncDB:
    
    def __init__(self, username, password):
        self.api = DeliciousAPI(username, password)

    def _syncPost(self, post):
        save_date = dateutil.parser.parse(post['time'])
      
        try:
            shared = post['shared']
        except KeyError:
            shared = True
        finally:
            if shared == 'no': shared = False
            
        d = {
            'title': post['description'], 
            'url': post['href'],
            'tags': post['tag'],
            'notes': post['extended'],
            'post_hash': post['hash'],
            'post_meta': post['meta'],
            'save_date': save_date,
            'shared': shared
        }
            
        b, created = Bookmark.objects.get_or_create(post_hash = d['post_hash'], defaults = d)
        if created == False:
            if not b.post_meta == unicode(d['post_meta']):
                b = Bookmark(
                        id=b.id,
                        title=d['title'],
                        url=d['url'],
                        tags=d['tags'],
                        notes=d['notes'],
                        post_hash=d['post_hash'],
                        post_meta=d['post_meta'],
                        save_date=d['save_date'],
                        shared=d['shared']
                     )
                b.save()
                
    def syncRecent(self, results='15'):
        posts = self.api.posts_all(results = 'results')
        for post in posts['posts']:
            self._syncPost(post)
        