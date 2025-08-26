from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import random

from app.models.user import User
from app.models.customer import CustomerStats
from app.services.auth_service import get_current_user
from app.services.customer_service import get_customer_stats, get_all_customers

router = APIRouter()
security = HTTPBearer()

def get_network_stats() -> Dict[str, Any]:
    """Generate mock network statistics"""
    return {
        "total_devices": 127,
        "online_devices": 119,
        "offline_devices": 8,
        "alerts": 3,
        "bandwidth_usage": {
            "total_mbps": 2847.5,
            "upload_mbps": 1203.2,
            "download_mbps": 1644.3
        },
        "signal_quality": {
            "excellent": 89,
            "good": 28,
            "fair": 8,
            "poor": 2
        }
    }

def get_revenue_stats() -> Dict[str, Any]:
    """Generate mock revenue statistics"""
    customers = get_all_customers()
    active_customers = [c for c in customers if c.status.value == "active"]
    
    monthly_revenue = sum(c.monthly_fee for c in active_customers)
    overdue_amount = sum(c.balance_due for c in customers if c.balance_due > 0)
    
    return {
        "monthly_revenue": monthly_revenue,
        "yearly_revenue": monthly_revenue * 12,
        "overdue_amount": overdue_amount,
        "collection_rate": 94.2,
        "average_revenue_per_user": monthly_revenue / len(active_customers) if active_customers else 0,
        "payment_methods": {
            "bank_transfer": 45.2,
            "cash": 28.7,
            "card": 18.5,
            "online": 7.6
        }
    }

def get_recent_activities() -> List[Dict[str, Any]]:
    """Generate mock recent activities"""
    activities = [
        {
            "id": 1,
            "type": "customer_signup",
            "title": "New Customer Registration",
            "description": "Patricia López Jiménez registered for Wireless Básico 25 Mbps",
            "timestamp": datetime.now() - timedelta(minutes=15),
            "severity": "info",
            "icon": "user-plus"
        },
        {
            "id": 2,
            "type": "payment_received",
            "title": "Payment Received",
            "description": "Payment of $899.00 received from María González Pérez",
            "timestamp": datetime.now() - timedelta(hours=2),
            "severity": "success",
            "icon": "dollar-sign"
        },
        {
            "id": 3,
            "type": "network_alert",
            "title": "Network Alert",
            "description": "High bandwidth usage detected in Sector 2 (>90%)",
            "timestamp": datetime.now() - timedelta(hours=4),
            "severity": "warning",
            "icon": "alert-triangle"
        },
        {
            "id": 4,
            "type": "equipment_offline",
            "title": "Equipment Offline",
            "description": "RB4011-Cozumel reported offline, technician dispatched",
            "timestamp": datetime.now() - timedelta(hours=6),
            "severity": "error",
            "icon": "wifi-off"
        },
        {
            "id": 5,
            "type": "customer_support",
            "title": "Support Ticket Resolved",
            "description": "Internet connectivity issue resolved for Carlos Mendoza",
            "timestamp": datetime.now() - timedelta(hours=8),
            "severity": "success",
            "icon": "check-circle"
        }
    ]
    return activities

def get_performance_metrics() -> Dict[str, Any]:
    """Generate mock performance metrics"""
    return {
        "system_health": {
            "cpu_usage": 23.5,
            "memory_usage": 67.2,
            "disk_usage": 45.8,
            "network_throughput": 847.3
        },
        "service_quality": {
            "uptime_percentage": 99.7,
            "average_response_time": 12.3,
            "customer_satisfaction": 4.6,
            "resolution_time": 2.4
        },
        "growth_metrics": {
            "new_customers_this_month": 12,
            "churn_rate": 2.1,
            "upgrade_rate": 8.7,
            "referral_rate": 15.3
        }
    }

@router.get("/overview")
async def get_dashboard_overview(
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get complete dashboard overview data"""
    customer_stats = get_customer_stats()
    network_stats = get_network_stats()
    revenue_stats = get_revenue_stats()
    recent_activities = get_recent_activities()
    performance_metrics = get_performance_metrics()
    
    return {
        "user": {
            "name": current_user.full_name,
            "role": current_user.role,
            "last_login": current_user.last_login,
            "department": current_user.department
        },
        "customers": customer_stats.dict(),
        "network": network_stats,
        "revenue": revenue_stats,
        "activities": recent_activities[:10],  # Last 10 activities
        "performance": performance_metrics,
        "timestamp": datetime.now()
    }

@router.get("/stats/customers")
async def get_dashboard_customer_stats(
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get customer statistics"""
    return get_customer_stats()

@router.get("/stats/network")
async def get_dashboard_network_stats(
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get network statistics"""
    return get_network_stats()

@router.get("/stats/revenue")
async def get_dashboard_revenue_stats(
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get revenue statistics"""
    return get_revenue_stats()

@router.get("/activities")
async def get_recent_activities_endpoint(
    limit: int = 20,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get recent system activities"""
    activities = get_recent_activities()
    return {
        "activities": activities[:limit],
        "total": len(activities),
        "timestamp": datetime.now()
    }

@router.get("/metrics")
async def get_performance_metrics_endpoint(
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get system performance metrics"""
    return get_performance_metrics()

# Chart data endpoints
@router.get("/charts/revenue-trend")
async def get_revenue_trend(
    days: int = 30,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get revenue trend data for charts"""
    # Generate mock trend data
    trend_data = []
    base_revenue = 50000
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        revenue = base_revenue + random.randint(-5000, 8000)
        trend_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "revenue": revenue,
            "customers": 120 + random.randint(-10, 15)
        })
    
    return {
        "data": trend_data,
        "period": f"Last {days} days",
        "total_revenue": sum(d["revenue"] for d in trend_data),
        "average_daily": sum(d["revenue"] for d in trend_data) / len(trend_data)
    }

@router.get("/charts/customer-growth")
async def get_customer_growth_chart(
    months: int = 12,
    current_user: User = Depends(lambda creds: get_current_user(creds.credentials)),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get customer growth data for charts"""
    growth_data = []
    base_customers = 80
    
    for i in range(months):
        month_date = datetime.now() - timedelta(days=30*(months-i-1))
        customers = base_customers + (i * 8) + random.randint(-3, 7)
        growth_data.append({
            "month": month_date.strftime("%Y-%m"),
            "total_customers": customers,
            "new_customers": random.randint(5, 15),
            "churned_customers": random.randint(1, 4)
        })
    
    return {
        "data": growth_data,
        "period": f"Last {months} months",
        "growth_rate": ((growth_data[-1]["total_customers"] - growth_data[0]["total_customers"]) / growth_data[0]["total_customers"] * 100) if growth_data else 0
    }