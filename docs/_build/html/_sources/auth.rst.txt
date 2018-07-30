Authentication
===============

passlib
--------
passlib provides an implementation of the SHA-256 hashing algorithm which is used to encrypt passwords.

flask-login
------------
This package is used to manage the logging in and logging out of users. All views that require user authentication 
should be marked with the `@login_required` decorator. Any attempts to access protected pages will result in a 
redirect to /login.

.. literalinclude:: ../vinceladotcom/auth.py