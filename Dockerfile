# Dockerfile
FROM nginx:alpine

# Copy the built static files from Vite's output folder
COPY dist /usr/share/nginx/html

# Security + performance
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/security.conf

# Optional: better caching for JS/CSS/assets
RUN echo '\
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?|ttf)$ { \
        expires 30d; \
        add_header Cache-Control "public"; \
    }' > /etc/nginx/conf.d/cache.conf