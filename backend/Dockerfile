# =================================================================
# N2P-CRM01 Backend Dockerfile
# Multi-stage build for production optimization
# =================================================================

# =================================================================
# Stage 1: Base Python Environment
# =================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.6.1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 n2p && \
    mkdir -p /app && \
    chown n2p:n2p /app

WORKDIR /app

# =================================================================
# Stage 2: Dependencies Installation
# =================================================================
FROM base as dependencies

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# =================================================================
# Stage 3: Development Environment
# =================================================================
FROM dependencies as development

# Install development dependencies
RUN pip install \
    pytest==7.4.3 \
    pytest-asyncio==0.21.1 \
    pytest-cov==4.1.0 \
    black==23.11.0 \
    isort==5.12.0 \
    flake8==6.1.0 \
    mypy==1.7.1

# Switch to non-root user
USER n2p

# Copy application code
COPY --chown=n2p:n2p . .

# Expose port
EXPOSE 8000

# Development command with hot reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]

# =================================================================
# Stage 4: Production Environment
# =================================================================
FROM dependencies as production

# Create directories for logs and data
RUN mkdir -p /app/logs /app/static /app/uploads && \
    chown -R n2p:n2p /app

# Switch to non-root user
USER n2p

# Copy application code (exclude development files)
COPY --chown=n2p:n2p app/ ./app/
COPY --chown=n2p:n2p main.py .
COPY --chown=n2p:n2p static/ ./static/
COPY --chown=n2p:n2p alembic.ini .
COPY --chown=n2p:n2p alembic/ ./alembic/

# Set production environment
ENV ENVIRONMENT=production \
    DEBUG=false

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Production command with gunicorn
CMD ["gunicorn", "main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--keep-alive", "5", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--preload", \
     "--log-level", "info", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

# =================================================================
# Stage 5: Testing Environment
# =================================================================
FROM development as testing

# Copy test files
COPY --chown=n2p:n2p tests/ ./tests/
COPY --chown=n2p:n2p pytest.ini .
COPY --chown=n2p:n2p .coveragerc .

# Run tests
CMD ["python", "-m", "pytest", "tests/", "-v", "--cov=app", "--cov-report=term-missing", "--cov-report=html"]

# =================================================================
# Build Arguments and Labels
# =================================================================
ARG BUILD_DATE
ARG VERSION=1.0.0
ARG VCS_REF

LABEL maintainer="Net2Point Engineering Team <support@net2point.com>" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="N2P-CRM01 Backend" \
      org.label-schema.description="Advanced ISP Management System Backend API" \
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
# docker build --target development -t n2p-crm01-backend:dev .
#
# Production:
# docker build --target production -t n2p-crm01-backend:latest .
#
# Testing:
# docker build --target testing -t n2p-crm01-backend:test .
# =================================================================