// Servicio para conectar con el backend N2P-CRM01
const API_BASE = 'http://127.0.0.1:8000';

export interface Customer {
  id: string;
  name: string;
  email?: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  service_type: string;
  plan_name: string;
  monthly_fee: number;
  status: string;
  payment_status: string;
  customer_number: string;
  created_at: string;
  updated_at: string;
  last_payment?: string;
  total_paid: number;
  balance_due: number;
  ip_address?: string;
  mac_address?: string;
  router_name?: string;
  signal_strength?: number;
  latitude?: number;
  longitude?: number;
  installation_date?: string;
  notes?: string;
}

export interface CustomerStats {
  total_customers: number;
  active_customers: number;
  suspended_customers: number;
  pending_customers: number;
  monthly_revenue: number;
  overdue_payments: number;
  new_customers_this_month: number;
}

export interface ApiInfo {
  name: string;
  version: string;
  status: string;
  mode: string;
  features: {
    authentication: string;
    customer_management: string;
    dashboard: string;
    health_check: string;
    api_documentation: string;
  };
  server_time: string;
  message: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
  timestamp: string;
  advanced_mode: boolean;
}

export interface SampleDataResponse {
  message: string;
  sample_customer: Customer;
  statistics: CustomerStats;
  total_customers: number;
  service_types: string[];
  customer_statuses: string[];
  payment_statuses: string[];
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Health check
  async getHealth(): Promise<HealthStatus> {
    return this.request<HealthStatus>('/health');
  }

  // API info
  async getApiInfo(): Promise<ApiInfo> {
    return this.request<ApiInfo>('/info');
  }

  // Obtener datos demo de clientes (endpoint público)
  async getCustomerSampleData(): Promise<SampleDataResponse> {
    return this.request<SampleDataResponse>('/api/v1/customers/demo/sample-data');
  }

  // Login (para uso futuro)
  async login(username: string, password: string) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  // Demo credentials
  async getDemoCredentials() {
    return this.request('/auth/demo-credentials');
  }
}

// Instancia singleton del cliente API
export const api = new ApiClient();

// Funciones de utilidad
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN',
    minimumFractionDigits: 0,
  }).format(amount);
};

export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

export const getServiceTypeLabel = (serviceType: string): string => {
  const labels: { [key: string]: string } = {
    fiber: 'Fibra Óptica',
    wireless: 'Inalámbrico',
    hybrid: 'Híbrido',
  };
  return labels[serviceType] || serviceType;
};

export const getStatusLabel = (status: string): string => {
  const labels: { [key: string]: string } = {
    active: 'Activo',
    suspended: 'Suspendido',
    inactive: 'Inactivo',
    pending: 'Pendiente',
  };
  return labels[status] || status;
};

export const getPaymentStatusLabel = (status: string): string => {
  const labels: { [key: string]: string } = {
    current: 'Al Corriente',
    overdue: 'Vencido',
    suspended: 'Suspendido',
  };
  return labels[status] || status;
};

export const getStatusColor = (status: string): string => {
  const colors: { [key: string]: string } = {
    active: 'bg-green-100 text-green-800',
    suspended: 'bg-red-100 text-red-800',
    inactive: 'bg-gray-100 text-gray-800',
    pending: 'bg-yellow-100 text-yellow-800',
    current: 'bg-green-100 text-green-800',
    overdue: 'bg-red-100 text-red-800',
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
};