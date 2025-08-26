from fastapi import APIRouter
from app.api.v1 import customers, dashboard

router = APIRouter()

# Include all v1 routes
router.include_router(customers.router, prefix="/customers", tags=["Customers"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Root endpoint for API v1
@router.get("/")
async def api_v1_root():
    """API v1 root endpoint"""
    return {
        "message": "N2P-CRM01 API v1",
        "version": "1.0.0",
        "endpoints": {
            "authentication": "/auth/login",
            "customers": "/api/v1/customers",
            "dashboard": "/api/v1/dashboard", 
            "demo_credentials": "/auth/demo-credentials",
            "sample_data": "/api/v1/customers/demo/sample-data"
        },
        "documentation": "/docs",
        "health_check": "/health"
    }

@router.get("/info")
async def api_info():
    """Get API information and available endpoints"""
    return {
        "api_name": "N2P-CRM01 ISP Management API",
        "version": "1.0.0",
        "description": "Advanced ISP/TSP Management System API",
        "features": [
            "User Authentication (JWT)",
            "Customer Management",
            "Dashboard Analytics", 
            "Network Monitoring (Mikrotik)",
            "Revenue Tracking",
            "Real-time Statistics"
        ],
        "endpoints": {
            "POST /auth/login": "Authenticate user and get JWT token",
            "GET /auth/me": "Get current user info",
            "GET /auth/demo-credentials": "Get demo login credentials",
            "GET /api/v1/customers": "List all customers",
            "GET /api/v1/customers/stats": "Get customer statistics", 
            "POST /api/v1/customers": "Create new customer",
            "GET /api/v1/customers/{id}": "Get customer by ID",
            "GET /api/v1/dashboard/overview": "Get dashboard overview",
            "GET /api/v1/dashboard/activities": "Get recent activities",
            "GET /api/v1/dashboard/charts/revenue-trend": "Revenue trend data"
        },
        "authentication": {
            "type": "Bearer JWT",
            "header": "Authorization: Bearer <token>",
            "demo_users": [
                {"username": "admin", "password": "admin123", "role": "Administrator"},
                {"username": "manager", "password": "manager123", "role": "Manager"}, 
                {"username": "tech", "password": "tech123", "role": "Technician"}
            ]
        },
        "sample_usage": {
            "login": "POST /auth/login with {username: 'admin', password: 'admin123'}",
            "get_customers": "GET /api/v1/customers with Authorization header",
            "dashboard": "GET /api/v1/dashboard/overview with Authorization header"
        }
    }