from typing import List, Optional
from datetime import datetime, timedelta
import random
import string
from app.models.customer import (
    Customer, CustomerCreate, CustomerUpdate, CustomerStats,
    CustomerStatus, ServiceType, PaymentStatus, CustomerFilter
)

# In-memory customer storage (later replace with database)
fake_customers_db = {}

def generate_customer_number() -> str:
    """Generate unique customer number"""
    return f"N2P{datetime.now().year}{random.randint(1000, 9999)}"

def create_demo_customers():
    """Create demo customers for testing"""
    demo_customers = [
        {
            "name": "María González Pérez",
            "email": "maria.gonzalez@email.com",
            "phone": "+52 998 123 0001",
            "address": "Av. Cobá #123, Cancún",
            "city": "Cancún",
            "state": "Quintana Roo",
            "zip_code": "77500",
            "service_type": ServiceType.FIBER,
            "plan_name": "Fibra Premium 100 Mbps",
            "monthly_fee": 899.00,
            "installation_date": datetime.now() - timedelta(days=120),
            "notes": "Cliente premium, sin issues reportados",
            "ip_address": "192.168.1.100",
            "mac_address": "AA:BB:CC:DD:EE:01",
            "router_name": "RB4011-Sector1",
            "signal_strength": 95,
            "latitude": 21.1619,
            "longitude": -86.8515
        },
        {
            "name": "Carlos Mendoza Ruiz",
            "email": "carlos.mendoza@empresa.com",
            "phone": "+52 998 123 0002", 
            "address": "Calle 15 #456, Playa del Carmen",
            "city": "Playa del Carmen",
            "state": "Quintana Roo",
            "zip_code": "77710",
            "service_type": ServiceType.WIRELESS,
            "plan_name": "Wireless Business 50 Mbps",
            "monthly_fee": 1299.00,
            "installation_date": datetime.now() - timedelta(days=89),
            "notes": "Cliente empresarial, requiere soporte 24/7",
            "ip_address": "192.168.2.150",
            "mac_address": "AA:BB:CC:DD:EE:02",
            "router_name": "RB4011-Sector2",
            "signal_strength": 87,
            "latitude": 20.6296,
            "longitude": -87.0739
        },
        {
            "name": "Ana Isabel Vargas",
            "email": "ana.vargas@hotmail.com",
            "phone": "+52 998 123 0003",
            "address": "Fraccionamiento Las Palmas #789",
            "city": "Cancún",
            "state": "Quintana Roo", 
            "zip_code": "77533",
            "service_type": ServiceType.FIBER,
            "plan_name": "Fibra Hogar 50 Mbps",
            "monthly_fee": 549.00,
            "installation_date": datetime.now() - timedelta(days=45),
            "notes": "Instalación reciente, muy satisfecha",
            "ip_address": "192.168.1.101",
            "mac_address": "AA:BB:CC:DD:EE:03",
            "router_name": "RB4011-Sector1",
            "signal_strength": 92,
            "latitude": 21.1743,
            "longitude": -86.8466
        },
        {
            "name": "Roberto Silva Martinez",
            "email": "roberto.silva@gmail.com",
            "phone": "+52 998 123 0004",
            "address": "Col. Centro, Calle Principal #321",
            "city": "Cozumel",
            "state": "Quintana Roo",
            "zip_code": "77600",
            "service_type": ServiceType.HYBRID,
            "plan_name": "Híbrido Empresarial 75 Mbps",
            "monthly_fee": 999.00,
            "installation_date": datetime.now() - timedelta(days=200),
            "notes": "Cliente de larga data, siempre puntual en pagos",
            "ip_address": "192.168.3.200",
            "mac_address": "AA:BB:CC:DD:EE:04",
            "router_name": "RB4011-Cozumel",
            "signal_strength": 89,
            "latitude": 20.5085,
            "longitude": -86.9461
        },
        {
            "name": "Patricia López Jiménez",
            "email": "paty.lopez@yahoo.com",
            "phone": "+52 998 123 0005",
            "address": "SM 21, Manzana 10, Lote 5",
            "city": "Cancún", 
            "state": "Quintana Roo",
            "zip_code": "77505",
            "service_type": ServiceType.WIRELESS,
            "plan_name": "Wireless Básico 25 Mbps",
            "monthly_fee": 399.00,
            "installation_date": datetime.now() - timedelta(days=15),
            "notes": "Nueva instalación, requiere seguimiento",
            "ip_address": "192.168.2.151",
            "mac_address": "AA:BB:CC:DD:EE:05",
            "router_name": "RB4011-Sector2",
            "signal_strength": 78,
            "latitude": 21.1508,
            "longitude": -86.8369
        }
    ]
    
    # Create customers with proper IDs and status
    for i, customer_data in enumerate(demo_customers, 1):
        customer_id = str(i)
        customer = Customer(
            id=customer_id,
            customer_number=generate_customer_number(),
            status=CustomerStatus.ACTIVE if i <= 4 else CustomerStatus.PENDING,
            payment_status=PaymentStatus.CURRENT if i <= 3 else PaymentStatus.OVERDUE,
            created_at=customer_data["installation_date"],
            updated_at=datetime.now(),
            last_payment=datetime.now() - timedelta(days=random.randint(5, 30)),
            total_paid=customer_data["monthly_fee"] * random.randint(2, 8),
            balance_due=customer_data["monthly_fee"] if i > 3 else 0.0,
            **customer_data
        )
        fake_customers_db[customer_id] = customer
    
    return len(fake_customers_db)

def get_all_customers() -> List[Customer]:
    """Get all customers"""
    return list(fake_customers_db.values())

def get_customer_by_id(customer_id: str) -> Optional[Customer]:
    """Get customer by ID"""
    return fake_customers_db.get(customer_id)

def create_customer(customer_data: CustomerCreate) -> Customer:
    """Create new customer"""
    customer_id = str(len(fake_customers_db) + 1)
    
    customer = Customer(
        id=customer_id,
        customer_number=generate_customer_number(),
        status=CustomerStatus.PENDING,
        payment_status=PaymentStatus.CURRENT,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        **customer_data.dict()
    )
    
    fake_customers_db[customer_id] = customer
    return customer

def update_customer(customer_id: str, customer_data: CustomerUpdate) -> Optional[Customer]:
    """Update existing customer"""
    if customer_id not in fake_customers_db:
        return None
    
    customer = fake_customers_db[customer_id]
    update_data = customer_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    customer.updated_at = datetime.now()
    fake_customers_db[customer_id] = customer
    
    return customer

def delete_customer(customer_id: str) -> bool:
    """Delete customer"""
    if customer_id in fake_customers_db:
        del fake_customers_db[customer_id]
        return True
    return False

def get_customer_stats() -> CustomerStats:
    """Get customer statistics"""
    customers = list(fake_customers_db.values())
    
    total_customers = len(customers)
    active_customers = len([c for c in customers if c.status == CustomerStatus.ACTIVE])
    suspended_customers = len([c for c in customers if c.status == CustomerStatus.SUSPENDED])
    pending_customers = len([c for c in customers if c.status == CustomerStatus.PENDING])
    
    monthly_revenue = sum(c.monthly_fee for c in customers if c.status == CustomerStatus.ACTIVE)
    overdue_payments = len([c for c in customers if c.payment_status == PaymentStatus.OVERDUE])
    
    # New customers this month
    current_month = datetime.now().replace(day=1)
    new_customers_this_month = len([
        c for c in customers 
        if c.created_at >= current_month
    ])
    
    return CustomerStats(
        total_customers=total_customers,
        active_customers=active_customers,
        suspended_customers=suspended_customers,
        pending_customers=pending_customers,
        monthly_revenue=monthly_revenue,
        overdue_payments=overdue_payments,
        new_customers_this_month=new_customers_this_month
    )

def search_customers(query: str, limit: int = 50) -> List[Customer]:
    """Search customers by name, email, phone, or address"""
    query = query.lower()
    customers = list(fake_customers_db.values())
    
    results = []
    for customer in customers:
        if (query in customer.name.lower() or
            query in customer.email.lower() if customer.email else False or
            query in customer.phone.lower() or
            query in customer.address.lower() or
            query in customer.city.lower() or
            query in customer.customer_number.lower()):
            results.append(customer)
    
    return results[:limit]

def filter_customers(filters: CustomerFilter) -> List[Customer]:
    """Filter customers by various criteria"""
    customers = list(fake_customers_db.values())
    
    if filters.status:
        customers = [c for c in customers if c.status == filters.status]
    
    if filters.service_type:
        customers = [c for c in customers if c.service_type == filters.service_type]
    
    if filters.payment_status:
        customers = [c for c in customers if c.payment_status == filters.payment_status]
    
    if filters.city:
        customers = [c for c in customers if c.city.lower() == filters.city.lower()]
    
    if filters.plan_name:
        customers = [c for c in customers if filters.plan_name.lower() in c.plan_name.lower()]
    
    if filters.overdue_only:
        customers = [c for c in customers if c.payment_status == PaymentStatus.OVERDUE]
    
    return customers

# Initialize with demo data
def init_customer_service():
    """Initialize customer service with demo data"""
    if not fake_customers_db:  # Only create if empty
        return create_demo_customers()
    return len(fake_customers_db)