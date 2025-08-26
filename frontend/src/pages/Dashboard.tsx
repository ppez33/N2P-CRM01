import React, { useState, useEffect } from 'react';
import { 
  api, 
  Customer, 
  CustomerStats, 
  SampleDataResponse,
  formatCurrency,
  formatDate,
  getServiceTypeLabel,
  getStatusLabel,
  getStatusColor
} from '../services/api';

const Dashboard: React.FC = () => {
  const [customerData, setCustomerData] = useState<SampleDataResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getCustomerSampleData();
      setCustomerData(data);
    } catch (err) {
      setError('Error cargando datos del CRM');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando N2P-CRM01...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-red-600 mb-2">Error de Conexión</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <p className="text-sm text-gray-500 mb-4">
            Asegúrate de que el backend esté ejecutándose en http://127.0.0.1:8000
          </p>
          <button 
            onClick={loadData}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  const stats = customerData?.statistics;
  const sampleCustomer = customerData?.sample_customer;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-gray-900 to-blue-900 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-4xl font-bold text-white">N2P-CRM01</h1>
              <p className="text-blue-200 mt-1">Sistema de Gestión ISP/TSP Avanzado</p>
            </div>
            <div className="text-right">
              <div className="flex items-center text-green-400">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse mr-2"></div>
                <span className="font-medium">Sistema Activo</span>
              </div>
              <p className="text-blue-200 text-sm">Cancún, Quintana Roo, México</p>
            </div>
          </div>
        </div>
      </header>

      {/* Dashboard Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white overflow-hidden shadow-lg rounded-lg hover:shadow-xl transition-shadow">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Clientes
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {stats?.total_customers || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow-lg rounded-lg hover:shadow-xl transition-shadow">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Clientes Activos
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {stats?.active_customers || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow-lg rounded-lg hover:shadow-xl transition-shadow">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Ingresos Mensuales
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {formatCurrency(stats?.monthly_revenue || 0)}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow-lg rounded-lg hover:shadow-xl transition-shadow">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Pagos Vencidos
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {stats?.overdue_payments || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sample Customer Card */}
        {sampleCustomer && (
          <div className="bg-white shadow-lg rounded-lg mb-8 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 px-6 py-4">
              <h3 className="text-xl font-bold text-white">Cliente Destacado</h3>
              <p className="text-blue-100 text-sm">Información detallada del cliente</p>
            </div>
            <div className="px-6 py-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Customer Info */}
                <div>
                  <div className="flex items-start space-x-4">
                    <div className="w-16 h-16 bg-blue-500 rounded-lg flex items-center justify-center">
                      <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                    <div className="flex-1">
                      <h4 className="text-xl font-bold text-gray-900">{sampleCustomer.name}</h4>
                      <p className="text-gray-600 mt-1">#{sampleCustomer.customer_number}</p>
                      <div className="mt-2">
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(sampleCustomer.status)}`}>
                          {getStatusLabel(sampleCustomer.status)}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-6 space-y-3">
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <div>
                        <p className="text-gray-900">{sampleCustomer.address}</p>
                        <p className="text-gray-600 text-sm">{sampleCustomer.city}, {sampleCustomer.state} {sampleCustomer.zip_code}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                      </svg>
                      <p className="text-gray-900">{sampleCustomer.phone}</p>
                    </div>
                    
                    {sampleCustomer.email && (
                      <div className="flex items-center">
                        <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 7.89a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                        <p className="text-gray-900">{sampleCustomer.email}</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Service Info */}
                <div>
                  <h5 className="text-lg font-semibold text-gray-900 mb-4">Información del Servicio</h5>
                  <div className="space-y-4">
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-sm font-medium text-gray-600">Plan Contratado</span>
                        <span className="text-lg font-bold text-green-600">{formatCurrency(sampleCustomer.monthly_fee)}/mes</span>
                      </div>
                      <p className="text-gray-900 font-medium">{sampleCustomer.plan_name}</p>
                      <p className="text-gray-600 text-sm">{getServiceTypeLabel(sampleCustomer.service_type)}</p>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-blue-50 rounded-lg p-3">
                        <p className="text-sm text-blue-600 font-medium">IP Asignada</p>
                        <p className="text-blue-900 font-mono">{sampleCustomer.ip_address}</p>
                      </div>
                      <div className="bg-green-50 rounded-lg p-3">
                        <p className="text-sm text-green-600 font-medium">Señal</p>
                        <p className="text-green-900 font-bold">{sampleCustomer.signal_strength}%</p>
                      </div>
                    </div>
                    
                    <div className="bg-gray-50 rounded-lg p-3">
                      <p className="text-sm text-gray-600 font-medium">Router</p>
                      <p className="text-gray-900">{sampleCustomer.router_name}</p>
                      <p className="text-gray-600 text-xs font-mono">{sampleCustomer.mac_address}</p>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Total Pagado</p>
                        <p className="text-lg font-bold text-gray-900">{formatCurrency(sampleCustomer.total_paid)}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Estado de Pago</p>
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(sampleCustomer.payment_status)}`}>
                          {getStatusLabel(sampleCustomer.payment_status)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              {sampleCustomer.notes && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <h6 className="text-sm font-medium text-gray-900 mb-2">Notas</h6>
                  <p className="text-gray-600 text-sm bg-yellow-50 p-3 rounded-lg">{sampleCustomer.notes}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* System Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Service Types */}
          <div className="bg-white shadow-lg rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Tipos de Servicio</h3>
            <div className="space-y-3">
              {customerData?.service_types?.map((type) => (
                <div key={type} className="flex justify-between items-center">
                  <span className="text-gray-600">{getServiceTypeLabel(type)}</span>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                    Disponible
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* System Status */}
          <div className="bg-white shadow-lg rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Estado del Sistema</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">99.9%</div>
                <div className="text-sm text-gray-600">Uptime</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{stats?.total_customers || 0}</div>
                <div className="text-sm text-gray-600">Clientes Totales</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">v1.0</div>
                <div className="text-sm text-gray-600">API Version</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">Online</div>
                <div className="text-sm text-gray-600">Backend Status</div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center">
          <p className="text-gray-500 text-sm">
            N2P-CRM01 Sistema de Gestión ISP/TSP • Net2Point Engineering Team • Cancún, Quintana Roo, México
          </p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;