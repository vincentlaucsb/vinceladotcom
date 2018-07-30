Nginx + uWSGI Deployment Notes
===============================

nginx Server Configuration
---------------------------

.. code-block:: none

    server {
        listen 80;
        server_name 107.170.208.132 vincela.com;
        
        ...
        
        # Flask App Documentation
        location /docs/ {
            alias /home/vinceladotcom/docs/_build/html/;
        }
        
        location /home/vinceladotcom/docs/_build/html/ {
            autoindex on;
        }
        
        # Flask    
        location / {
            location /static/ {
                root /home/vinceladotcom/vinceladotcom/;
                autoindex on;
            }

            include uwsgi_params;
            uwsgi_pass unix:///home/vinceladotcom/myproject.sock;
        }

        ...
        
    }
    
uWSGI Notes
------------
wsgi.py serves as the main entry point to the web app. Because uWSGI is anal, it precisely expects a global variable called `application` to be present.

.. literalinclude:: ../../vinceladotcom/wsgi.py