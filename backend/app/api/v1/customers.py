from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.customer import (
    Customer, CustomerCreate, CustomerUpdate, CustomerStats, 
    CustomerFilter, ServiceType, CustomerStatus, PaymentStatus
)
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.customer_service import (
    get_all_customers, get_customer_by_id, create_customer, 
    update_customer, delete_customer, get_customer_stats,
    search_customers, filter_customers, init_customer_service
)

router = APIRouter()
security = HTTPBearer()

# Initialize demo data
init_customer_service()

@router.get("/", response_model=List[Customer])
async def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials) if creds else None),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get all customers with pagination"""
    customers = get_all_customers()
    return customers[skip:skip + limit]

@router.get("/stats", response_model=CustomerStats)
async def get_customers_stats(
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get customer statistics for dashboard"""
    return get_customer_stats()

@router.get("/search")
async def search_customers_endpoint(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Search customers by name, email, phone, or address"""
    results = search_customers(q, limit)
    return {
        "query": q,
        "total_results": len(results),
        "customers": results
    }

@router.get("/filter")
async def filter_customers_endpoint(
    status: Optional[CustomerStatus] = None,
    service_type: Optional[ServiceType] = None,
    payment_status: Optional[PaymentStatus] = None,
    city: Optional[str] = None,
    plan_name: Optional[str] = None,
    overdue_only: bool = False,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Filter customers by various criteria"""
    filters = CustomerFilter(
        status=status,
        service_type=service_type,
        payment_status=payment_status,
        city=city,
        plan_name=plan_name,
        overdue_only=overdue_only
    )
    
    results = filter_customers(filters)
    return {
        "filters": filters.dict(exclude_none=True),
        "total_results": len(results),
        "customers": results
    }

@router.post("/", response_model=Customer)
async def create_new_customer(
    customer: CustomerCreate,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new customer"""
    return create_customer(customer)

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: str,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get customer by ID"""
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=404, 
            detail="Customer not found"
        )
    return customer

@router.put("/{customer_id}", response_model=Customer)
async def update_customer_endpoint(
    customer_id: str,
    customer_update: CustomerUpdate,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update customer information"""
    customer = update_customer(customer_id, customer_update)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return customer

@router.delete("/{customer_id}")
async def delete_customer_endpoint(
    customer_id: str,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Delete customer"""
    success = delete_customer(customer_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return {"message": "Customer deleted successfully"}

# Public endpoint for demo purposes (no auth required)
@router.get("/demo/sample-data")
async def get_sample_customer_data():
    """Get sample customer data structure (for frontend development)"""
    customers = get_all_customers()
    stats = get_customer_stats()
    
    return {
        "message": "Sample customer data for N2P-CRM01",
        "sample_customer": customers[0] if customers else None,
        "statistics": stats,
        "total_customers": len(customers),
        "service_types": [service.value for service in ServiceType],
        "customer_statuses": [status.value for status in CustomerStatus],
        "payment_statuses": [status.value for status in PaymentStatus]
    }