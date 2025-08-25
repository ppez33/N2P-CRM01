# =================================================================
# N2P-CRM01 Frontend Dockerfile
# Multi-stage build for optimized production bundle
# =================================================================

# =================================================================
# Stage 1: Base Node.js Environment
# =================================================================
FROM node:18-alpine as base

# Install system dependencies
RUN apk add --no-cache \
    libc6-compat \
    curl \
    git

# Set working directory
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# =================================================================
# Stage 2: Dependencies Installation
# =================================================================
FROM base as dependencies

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Install all dependencies (including dev)
FROM base as dev-dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# =================================================================
# Stage 3: Development Environment
# =================================================================
FROM dev-dependencies as development

# Copy source code
COPY --chown=nextjs:nodejs . .

# Change to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Development command with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]

# =================================================================
# Stage 4: Build Stage
# =================================================================
FROM dev-dependencies as builder

# Set build environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy source code
COPY . .

# Build application
RUN npm run build && \
    npm prune --production

# =================================================================
# Stage 5: Production Environment with Nginx
# =================================================================
FROM nginx:alpine as production

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create nginx user and set permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Create log directories
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx

# Copy SSL configuration template
COPY ssl.conf /etc/nginx/conf.d/ssl.conf.template

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Expose ports
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# =================================================================
# Stage 6: Node.js Production Server (Alternative)
# =================================================================
FROM base as node-production

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy production dependencies
COPY --from=dependencies /app/node_modules ./node_modules

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json

# Change to non-root user
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Expose port
EXPOSE 3000

# Start production server
CMD ["npm", "start"]

# =================================================================
# Nginx Configuration for Production
# =================================================================
# Create nginx.conf file with the following content:

# nginx.conf content (save as separate file):
---
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https: wss:;" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/js
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }

    # Handle client-side routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (if needed)
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://backend:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}

# SSL Configuration (ssl.conf.template)
server {
    listen 443 ssl http2;
    server_name _;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Include the same location blocks as HTTP server
    include /etc/nginx/conf.d/default.conf;
}

# =================================================================
# Build Arguments and Labels
# =================================================================
ARG BUILD_DATE
ARG VERSION=1.0.0
ARG VCS_REF

LABEL maintainer="Net2Point Engineering Team <support@net2point.com>" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="N2P-CRM01 Frontend" \
      org.label-schema.description="Advanced ISP Management System Frontend" \
      org.label-schema.url="https://github.com/ppez33/N2P-CRM01" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/ppez33/N2P-CRM01" \
      org.label-schema.vendor="Net2Point" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

# =================================================================
# Build Commands:
# =================================================================
# Development:
# docker build --target development -t n2p-crm01-frontend:dev .
#
# Production (Nginx):
# docker build --target production -t n2p-crm01-frontend:latest .
#
# Production (Node.js):
# docker build --target node-production -t n2p-crm01-frontend:node .
# =================================================================