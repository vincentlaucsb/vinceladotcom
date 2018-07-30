Blog Posts and (Mostly) Static Pages
======================================

Blogging and pages are implemented as separate Blueprints. However, they share many components in common.

Forms
------

This app defines additional custom fields in addition to the forms provided by WTForms which wrap the JavaScript-powered
ACE text editor. The AceText widget merely consists of a basic ACE text editor, while the AceTextPreview widget adds an
automatic updating preview.

.. toctree::
   forms

Revision History
-----------------

The SQLite database contains the tables `blogrevisions` and `pagerevisions` which contain all
past versions of blogs and pages respectively. These tables are automatically maintained by insert
triggers.
