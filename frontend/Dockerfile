# --- build ---
FROM node:20-alpine AS build
WORKDIR /app

# Copie uniquement les manifests pour maximiser le cache
COPY package.json package-lock.json* ./

# Si tu n'as PAS de package-lock.json, npm install; sinon npm ci
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copie le reste (src, vite.config.js, etc.)
COPY . .
RUN npm run build

# --- serve ---
FROM nginx:alpine
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
