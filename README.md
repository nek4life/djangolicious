# Djangolicious

Sync your delicious bookmarks to your Django project's database and back again to Delicious.

Example usage:

`from djangolicious.utils import DeliciousSyncDB

instance = DeliciousSyncDB('username', 'password')

instance.syncRecent(recent='15') # Syncs recent bookmarks recent argument optional defaults to 15
instance.syncAll() # Syncs all bookmarks
instance.processQueue() # Pushes locally modified objects that have been queued back to Delicious`

## Dependancies:

* pydelicious : http://code.google.com/p/pydelicious/
    * feedparser : http://www.feedparser.org/   
* django-tagging : http://code.google.com/p/django-tagging/

