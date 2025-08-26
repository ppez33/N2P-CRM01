import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.models.user import User, UserInDB, Token, LoginRequest, UserRole

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# In-memory user storage (later replace with database)
fake_users_db = {
    "admin": {
        "id": "1",
        "username": "admin",
        "email": "admin@net2point.com",
        "full_name": "Administrator",
        "role": UserRole.ADMIN,
        "is_active": True,
        "phone": "+52 998 123 4567",
        "department": "IT",
        "hashed_password": "$2b$12$lK/v6s1oukNYpBDf12sW1ewT4nzGb6iMB0TzyBRO3.nRHX8ouiyHS",  # "admin123"
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "last_login": None,
        "login_count": 0
    },
    "manager": {
        "id": "2", 
        "username": "manager",
        "email": "manager@net2point.com",
        "full_name": "Network Manager",
        "role": UserRole.MANAGER,
        "is_active": True,
        "phone": "+52 998 123 4568",
        "department": "Network Operations",
        "hashed_password": "$2b$12$O7CXg2GRxkDrieCeXdFyTeGhVuG.tNrvb9K88uYnfF9fcXO4jmqvu",  # "manager123"
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "last_login": None,
        "login_count": 0
    },
    "tech": {
        "id": "3",
        "username": "tech",
        "email": "tech@net2point.com", 
        "full_name": "Field Technician",
        "role": UserRole.TECHNICIAN,
        "is_active": True,
        "phone": "+52 998 123 4569",
        "department": "Field Operations", 
        "hashed_password": "$2b$12$3VXFrJ5WoT5//ScIhUb4netRr983gqldMI1nPcAYNJuNecanGvS6O",  # "tech123"
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "last_login": None,
        "login_count": 0
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def get_user(username: str) -> Optional[UserInDB]:
    """Get user by username"""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user credentials"""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    # Update login stats
    fake_users_db[username]["last_login"] = datetime.now()
    fake_users_db[username]["login_count"] += 1
    
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[str]:
    """Decode JWT token and return username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.PyJWTError:
        return None

def login(login_request: LoginRequest) -> Token:
    """Login user and return token"""
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Convert to public user model (without hashed_password)
    public_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        phone=user.phone,
        department=user.department,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        login_count=user.login_count
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user=public_user
    )

def get_current_user(token: str) -> User:
    """Get current user from token"""
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convert to public user model
    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        phone=user.phone,
        department=user.department,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        login_count=user.login_count
    )

# Demo function to create test users
def create_demo_users():
    """Create demo users for testing"""
    return {
        "admin": "admin123",
        "manager": "manager123", 
        "tech": "tech123"
    }