import time
import datetime
from pydelicious import DeliciousAPI

from djangolicious.models import Bookmark

class DeliciousSyncDB:
    
    def __init__(self, username, password):
        """
        Initializes the DeliciousSyncDB object.
        
        This functions accepts two arguments
        username and password. Both are required. 
        """
        self.api = DeliciousAPI(username, password)
        
    def _cleanTags(self, tags):
        """
        Utility function that sets tags to lower case, removes
        commas and double quotes and removes all duplicate tags.
        
        Returns a unicode string.  
        """
        tags = tags.lower().replace('\"', '').replace(',', '').split(' ')
        tags = set(tags)
        tags = ' '.join(tags)
        return u'%s' % tags
        
    def _syncPost(self, post):
        """
        Utility function that saves bookmarks to the
        local database.
        
        In the case a bookmark already exists it will be
        updated instead.
        """
        time_obj = time.strptime(post['time'], "%Y-%m-%dT%H:%M:%SZ")
        save_date = datetime.datetime(*time_obj[0:7])
        
        try:
            shared = post['shared']
        except KeyError:
            shared = True
        finally:
            if shared == 'no': shared = False
            
        tags = self._cleanTags(post['tag'])
        d = {
            'title': post['description'], 
            'url': post['href'],
            'tags': tags,
            'notes': post['extended'],
            'post_hash': post['hash'],
            'post_meta': post['meta'],
            'save_date': save_date,
            'shared': shared
        }
        
        b, created = Bookmark.objects.get_or_create(url = d['url'], defaults = d)
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
                b.save(syncAPI=True)
                
    def syncRecent(self, results=15):
        """
        Syncronizes recent Delicious boomarks to a
        local database.
        
        This uses the posts/all api call instead of
        using the posts/recent call. Doing so provides the
        meta attribute in order to update previously saved
        bookmarks with modified data from Delicious.
        
        syncRecent takes one argument for results. If not 
        specified the default number of results returned
        is 15.
        """
        posts = self.api.posts_all(results = str(results))
        for post in posts['posts']:
            self._syncPost(post)
            
    def syncAll(self):
        """
        Syncronizes all Delicious boomarks to a
        local database.
        
        Using the meta attribute previously saved bookmarks
        will also be updated as well.
        """
        posts = self.api.posts_all()
        for post in posts['posts']:
            self._syncPost(post)        
        
    def processQueue(self):
        """
        Queue processor to process local bookmarks that are
        going to be pushed to Delicious using posts/add.
        
        Bookmarks saved locally are flagged as queued and
        unflagged as they have been processed.
        
        If a boomark is unsucessfully updated the program will
        fail silently and move on to the next one until the
        entire queue has been processed once through.
        """
        bookmarks = Bookmark.objects.filter(queued=True)
        for bookmark in bookmarks:
            time.sleep(1.5)
            try:
                if bookmark.shared == False:
                    shared = 'no'
                else:
                    shared = 'yes'
                self.api.posts_add(
                        bookmark.url,
                        bookmark.title,
                        extended=bookmark.notes,
                        tags=bookmark.tags,
                        shared=shared,
                        replace='yes')
                bookmark.queued = False
                bookmark.save(syncAPI=True)
            except: 
                pass
