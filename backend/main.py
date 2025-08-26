#!/usr/bin/env python3
"""
N2P-CRM01 - ISP Management System
FastAPI Backend Application - WORKING VERSION
"""

import sys
import os
import logging
from datetime import datetime

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="N2P-CRM01 API",
    description="Advanced ISP/TSP Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to import advanced modules
try:
    from app.api.auth.router import router as auth_router
    from app.api.v1.router import router as api_router_v1
    from app.services.customer_service import init_customer_service
    
    # Include routers
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(api_router_v1, prefix="/api/v1", tags=["API v1"])
    
    # Initialize demo data
    customer_count = init_customer_service()
    logger.info(f"✅ CRM modules loaded successfully - {customer_count} demo customers")
    ADVANCED_MODE = True
    
except ImportError as e:
    logger.warning(f"⚠️ Advanced modules not available: {e}")
    logger.info("🔧 Running in basic mode")
    ADVANCED_MODE = False

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "N2P-CRM01 API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "advanced_mode": ADVANCED_MODE
    }

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    status_text = "🚀 ONLINE & FUNCTIONAL" if ADVANCED_MODE else "🔧 BASIC MODE"
    status_color = "#00ff00" if ADVANCED_MODE else "#ffaa00"
    
    links_html = ""
    if ADVANCED_MODE:
        links_html = '''
        <a href="/auth/demo-credentials" class="link">
            <strong>🔑 Demo Credentials</strong><br>
            Test Login Accounts
        </a>
        <a href="/api/v1/customers/demo/sample-data" class="link">
            <strong>📊 Sample Data</strong><br>
            Demo Customer Data
        </a>
        <a href="/auth/login" class="link">
            <strong>🔐 Login API</strong><br>
            Authentication Endpoint
        </a>
        <div class="credentials">
            <strong>🔑 Test Credentials:</strong><br>
            <code>admin / admin123</code> | <code>manager / manager123</code> | <code>tech / tech123</code>
        </div>
        '''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>N2P-CRM01 API Server</title>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #000000 0%, #197899 100%);
                color: white;
                margin: 0;
                padding: 20px;
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
                max-width: 900px;
                width: 100%;
            }}
            .logo {{
                font-size: 3.5rem;
                font-weight: bold;
                margin-bottom: 1rem;
                color: #14c4cd;
                text-shadow: 0 0 20px rgba(20, 196, 205, 0.5);
            }}
            .subtitle {{
                font-size: 1.3rem;
                margin-bottom: 2rem;
                opacity: 0.9;
            }}
            .status {{
                display: inline-block;
                background: {status_color};
                color: #000;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                font-weight: bold;
                margin-bottom: 2rem;
                font-size: 1.1rem;
            }}
            .links {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }}
            .link {{
                display: block;
                background: rgba(20, 196, 205, 0.15);
                color: #14c4cd;
                padding: 1.2rem;
                border-radius: 12px;
                text-decoration: none;
                border: 2px solid #14c4cd;
                transition: all 0.3s ease;
            }}
            .link:hover {{
                background: #14c4cd;
                color: #000;
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(20, 196, 205, 0.3);
            }}
            .credentials {{
                background: rgba(255, 255, 255, 0.1);
                padding: 1rem;
                border-radius: 10px;
                margin-top: 2rem;
                font-size: 1rem;
                border: 1px solid rgba(255,255,255,0.2);
            }}
            .footer {{
                margin-top: 2rem;
                font-size: 0.9rem;
                opacity: 0.7;
            }}
            code {{
                background: rgba(0,0,0,0.3);
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">N2P-CRM01</div>
            <div class="subtitle">ISP Management System API Server</div>
            <div class="status">{status_text}</div>
            
            <div class="links">
                <a href="/health" class="link">
                    <strong>💊 Health Check</strong><br>
                    System Status & Info
                </a>
                <a href="/docs" class="link">
                    <strong>📚 API Documentation</strong><br>
                    Interactive Swagger UI
                </a>
                <a href="/info" class="link">
                    <strong>ℹ️ API Info</strong><br>
                    Endpoints Overview
                </a>
                <a href="https://github.com/ppez33/N2P-CRM01" class="link" target="_blank">
                    <strong>🐙 GitHub Repository</strong><br>
                    Source Code & Documentation
                </a>
                {links_html}
            </div>
            
            <div class="footer">
                <strong>N2P-CRM01 v1.0.0</strong> | Advanced Mode: {"✅ Active" if ADVANCED_MODE else "⚠️ Basic"}<br>
                Net2Point Engineering Team © 2025<br>
                <strong>Cancún, Quintana Roo, México 🇲🇽</strong>
            </div>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)

# API info endpoint
@app.get("/info")
async def api_info():
    features = {
        "authentication": "✅ Available" if ADVANCED_MODE else "❌ Not available",
        "customer_management": "✅ Available" if ADVANCED_MODE else "❌ Not available", 
        "dashboard": "✅ Available" if ADVANCED_MODE else "❌ Not available",
        "health_check": "✅ Always available",
        "api_documentation": "✅ Always available"
    }
    
    return {
        "name": "N2P-CRM01 API",
        "version": "1.0.0",
        "status": "operational",
        "mode": "advanced" if ADVANCED_MODE else "basic",
        "features": features,
        "endpoints": {
            "health": "/health",
            "docs": "/docs", 
            "info": "/info"
        },
        "server_time": datetime.now().isoformat(),
        "message": "CRM API is running successfully!" if ADVANCED_MODE else "Server running in basic mode"
    }

# Basic demo endpoint
@app.get("/demo")
async def demo_endpoint():
    return {
        "message": "N2P-CRM01 Demo Endpoint",
        "status": "working",
        "features": "CRM for ISP/TSP management",
        "mode": "advanced" if ADVANCED_MODE else "basic",
        "timestamp": datetime.now().isoformat()
    }

# Run server
if __name__ == "__main__":
    print("🚀 Starting N2P-CRM01 Server...")
    print("📖 Documentation: http://127.0.0.1:8000/docs")
    print("🌐 Web Interface: http://127.0.0.1:8000")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )