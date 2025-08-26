from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import Token, LoginRequest, User
from app.services.auth_service import login, get_current_user

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=Token)
async def login_user(login_request: LoginRequest):
    """
    Login endpoint - authenticate user and return JWT token
    
    Test credentials:
    - username: admin, password: admin123
    - username: manager, password: manager123  
    - username: tech, password: tech123
    """
    return login(login_request)

@router.get("/me", response_model=User)
async def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user information from token"""
    return get_current_user(credentials.credentials)

@router.post("/logout")
async def logout_user():
    """Logout endpoint (client should discard token)"""
    return {"message": "Successfully logged out"}

@router.get("/demo-credentials")
async def get_demo_credentials():
    """Get demo credentials for testing"""
    return {
        "message": "Demo credentials for N2P-CRM01",
        "credentials": [
            {
                "username": "admin",
                "password": "admin123",
                "role": "Administrator",
                "description": "Full system access"
            },
            {
                "username": "manager", 
                "password": "manager123",
                "role": "Network Manager",
                "description": "Network operations management"
            },
            {
                "username": "tech",
                "password": "tech123", 
                "role": "Field Technician",
                "description": "Field operations and customer support"
            }
        ],
        "usage": "POST /api/v1/auth/login with username and password"
    }