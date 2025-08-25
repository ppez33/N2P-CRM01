#!/usr/bin/env python3
"""
N2P-CRM01 - ISP Management System
FastAPI Backend Application
"""

import os
import sys
import logging
from pathlib import Path
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from contextlib import asynccontextmanager

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.core.database import init_database, close_database
from app.core.redis_client import init_redis, close_redis
from app.core.exceptions import setup_exception_handlers
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.security import SecurityMiddleware

# Import API routers
from app.api.v1.router import api_router_v1
from app.api.auth.router import auth_router
from app.api.health.router import health_router

# Initialize settings
settings = get_settings()

# Setup logging
logger = setup_logging()

# Application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting N2P-CRM01 Backend Server...")
    
    # Initialize database
    try:
        await init_database()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise
    
    # Initialize Redis
    try:
        await init_redis()
        logger.info("✅ Redis initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Redis: {e}")
        raise
    
    # Initialize AI models (if enabled)
    if settings.FEATURE_AI_MONITORING:
        try:
            from app.services.ai_monitoring.models import init_ai_models
            await init_ai_models()
            logger.info("✅ AI models initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize AI models: {e}")
    
    logger.info("🎯 N2P-CRM01 Backend Server started successfully")
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down N2P-CRM01 Backend Server...")
    
    # Close database connections
    try:
        await close_database()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")
    
    # Close Redis connections
    try:
        await close_redis()
        logger.info("✅ Redis connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing Redis: {e}")
    
    logger.info("✅ N2P-CRM01 Backend Server shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="N2P-CRM01 API",
    description="Advanced ISP/TSP Management System with AI Monitoring and Predictive Analytics",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT in ["development", "staging"] else None,
    lifespan=lifespan,
    contact={
        "name": "Net2Point Engineering Team",
        "url": "https://github.com/ppez33/N2P-CRM01",
        "email": "support@net2point.com"
    },
    license_info={
        "name": "Commercial License",
        "url": "https://github.com/ppez33/N2P-CRM01/blob/main/LICENSE"
    }
)

# Add security middleware
app.add_middleware(SecurityMiddleware)

# Add trusted host middleware
if settings.ALLOWED_HOSTS:
    allowed_hosts = [host.strip() for host in settings.ALLOWED_HOSTS.split(",")]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Add CORS middleware
if settings.CORS_ORIGINS:
    origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add rate limiting middleware
if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Setup exception handlers
setup_exception_handlers(app)

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(api_router_v1, prefix="/api/v1", tags=["API v1"])

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>N2P-CRM01 API Server</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #000000 0%, #197899 100%);
                color: white;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                text-align: center;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                backdrop-filter: blur(10px);
                max-width: 600px;
                margin: 2rem;
            }}
            .logo {{
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 1rem;
                color: #14c4cd;
            }}
            .subtitle {{
                font-size: 1.2rem;
                margin-bottom: 2rem;
                opacity: 0.9;
            }}
            .status {{
                display: inline-block;
                background: #00ff00;
                color: #000;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-weight: bold;
                margin-bottom: 2rem;
            }}
            .links {{
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
            }}
            .link {{
                display: inline-block;
                background: rgba(20, 196, 205, 0.2);
                color: #14c4cd;
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                text-decoration: none;
                border: 1px solid #14c4cd;
                transition: all 0.3s ease;
            }}
            .link:hover {{
                background: #14c4cd;
                color: #000;
                transform: translateY(-2px);
            }}
            .footer {{
                margin-top: 2rem;
                font-size: 0.9rem;
                opacity: 0.7;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">N2P-CRM01</div>
            <div class="subtitle">ISP Management System API Server</div>
            <div class="status">🚀 ONLINE</div>
            
            <div class="links">
                <a href="/health" class="link">Health Check</a>
                <a href="/docs" class="link">API Documentation</a>
                <a href="/api/v1" class="link">API v1</a>
                <a href="https://github.com/ppez33/N2P-CRM01" class="link" target="_blank">GitHub</a>
            </div>
            
            <div class="footer">
                Version {settings.APP_VERSION} | Environment: {settings.ENVIRONMENT}
                <br>
                Net2Point Engineering Team © 2025
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# API Info endpoint
@app.get("/info", response_model=dict)
async def api_info():
    """Get API information"""
    return {
        "name": "N2P-CRM01 API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "features": {
            "ai_monitoring": settings.FEATURE_AI_MONITORING,
            "bequant_integration": settings.FEATURE_BEQUANT_INTEGRATION,
            "gis_mapping": settings.FEATURE_GIS_MAPPING,
            "automated_billing": settings.FEATURE_AUTOMATED_BILLING,
            "whatsapp_notifications": settings.FEATURE_WHATSAPP_NOTIFICATIONS,
            "predictive_analytics": settings.FEATURE_PREDICTIVE_ANALYTICS
        },
        "documentation": "/docs",
        "health_check": "/health"
    }

# Development server runner
if __name__ == "__main__":
    # Only run with uvicorn in development
    if settings.ENVIRONMENT == "development":
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="debug",
            access_log=True
        )
    else:
        logger.warning("Use a production WSGI server (gunicorn) to run this application in production")