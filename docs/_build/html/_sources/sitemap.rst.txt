Sitemap Generator
===================

This web app contains a simple, rudimentary sitemap generator. Currently, there is one main 
sitemap at http://vincela.com/sitemap.xml

Populating the Sitemap
-----------------------

.. code-block:: python

    _sitemap = Sitemap(request.url_root)
    
    for post in database.BlogPost.select():
        entry = SitemapEntry()
        entry['loc'] = 'blog/' + post.url()
        entry['lastmod'] = post.modified
        _sitemap.add(entry)
        
The Sitemap Class
------------------

The Sitemap class is a wrapper around a list of SitemapEntry objects. These classes are 
based on built-in data structures and have methods for generating XML string representations. Each instance
of a Sitemap object to correspond to one sitemap.xml file.

.. literalinclude:: ../vinceladotcom/sitemap.py