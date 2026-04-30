FROM nginx:alpine

# Copy built Vite files
COPY dist /usr/share/nginx/html

# Basic security
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/security.conf