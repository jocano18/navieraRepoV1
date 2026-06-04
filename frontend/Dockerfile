# syntax=docker/dockerfile:1

FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci 2>/dev/null || npm install

FROM node:20-alpine AS development
# La imagen oficial ya incluye usuario "node" (uid 1000); no crear otro con el mismo gid.
RUN apk add --no-cache wget
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY docker-entrypoint.dev.sh /docker-entrypoint.dev.sh
COPY . .
RUN sed -i 's/\r$//' /docker-entrypoint.dev.sh \
    && chmod +x /docker-entrypoint.dev.sh \
    && chown -R node:node /app /docker-entrypoint.dev.sh \
    && touch node_modules/.install-stamp
USER node
EXPOSE 5173
ENTRYPOINT ["/docker-entrypoint.dev.sh"]

FROM node:20-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine AS production
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
