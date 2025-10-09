# Stage 1: Build
FROM node:20-alpine as builder

WORKDIR /app

# Copier les fichiers package
COPY package*.json ./

# Installer les dépendances
RUN npm install --production=false

# Copier le code source
COPY . .

# Build de l'application
RUN npm run build

# Stage 2: Production avec Nginx
FROM nginx:alpine

# Copier le build depuis le stage précédent
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuration nginx inline (pas besoin de fichier séparé)
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    \
    location /api/ { \
        proxy_pass http://backend:8000/; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_connect_timeout 300s; \
        proxy_send_timeout 300s; \
        proxy_read_timeout 300s; \
    } \
    \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Démarrer nginx
CMD ["nginx", "-g", "daemon off;"]