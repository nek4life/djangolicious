# Djangolicious

Sync your delicious bookmarks to your Django project's database and back again to Delicious.

Please note that this project is in it's early stages and is rapidly changing, so things could
potentially break from one update to another.  I will tag a 1.0 release as soon as I reach a
stable feature set.

Dependancies:

* feedparser : http://www.feedparser.org/ (required for pydelicious)
* pydelicious : http://code.google.com/p/pydelicious/
* django-tagging : http://code.google.com/p/django-tagging/
* Python-Markdown : http://pypi.python.org/pypi/Markdown
* Smartypants.py : http://web.chad.org/projects/smartypants.py/

Example usage:

    from djangolicious.utils import DeliciousSyncDB

    instance = DeliciousSyncDB('username', 'password')

    instance.syncRecent(recent='15') # Syncs recent bookmarks recent argument optional defaults to 15
    instance.syncAll() # Syncs all bookmarks
    instance.processQueue() # Pushes locally modified objects that have been queued back to Delicious

Todo:

* Add pruneDB function to clean up database when bookmarks are deleted from Delicious
