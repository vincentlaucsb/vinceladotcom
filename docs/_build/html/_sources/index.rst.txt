.. vinceladotcom documentation master file, created by
   sphinx-quickstart on Mon Jul 16 22:32:33 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

vinceladotcom Website Architecture
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

GitHub
-------
https://github.com/vincentlaucsb/vinceladotcom
   
Introduction
--------------
These were mainly written as notes to myself in case I forgot how my own website worked. However, they 
can also serve as a reference for anybody else interested in building a Flask web app.

Structure
----------
My website has several components:

.. toctree::
   auth
   
.. toctree::
   blog_pages
   
.. toctree::
   sitemap
   
SQLite
-------
Currently, SQLite is used as the database backend. In order to swap out SQLite for another database engine, one would have to rewrite the triggers which create blog/page revision histories.

Deployment
-----------

.. toctree::
   nginx
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
