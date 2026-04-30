FROM nginx:alpine

COPY . /usr/share/nginx/html

# Security
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/security.conf