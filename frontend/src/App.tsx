import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { HelmetProvider } from 'react-helmet-async';
import { ErrorBoundary } from 'react-error-boundary';
import { Toaster } from 'react-hot-toast';

// Context Providers
import { AuthProvider } from '@/contexts/AuthContext';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { SettingsProvider } from '@/contexts/SettingsContext';

// Layout Components
import { MainLayout } from '@/components/layout/MainLayout';
import { AuthLayout } from '@/components/layout/AuthLayout';

// Page Components
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorFallback } from '@/components/common/ErrorFallback';

// Lazy-loaded Pages
const Dashboard = React.lazy(() => import('@/pages/dashboard/Dashboard'));
const Login = React.lazy(() => import('@/pages/auth/Login'));
const Register = React.lazy(() => import('@/pages/auth/Register'));
const ForgotPassword = React.lazy(() => import('@/pages/auth/ForgotPassword'));

// Customer Management
const Customers = React.lazy(() => import('@/pages/clients/Customers'));
const CustomerDetail = React.lazy(() => import('@/pages/clients/CustomerDetail'));
const AddCustomer = React.lazy(() => import('@/pages/clients/AddCustomer'));

// Billing
const Invoices = React.lazy(() => import('@/pages/billing/Invoices'));
const InvoiceDetail = React.lazy(() => import('@/pages/billing/InvoiceDetail'));
const CreateInvoice = React.lazy(() => import('@/pages/billing/CreateInvoice'));
const Payments = React.lazy(() => import('@/pages/billing/Payments'));

// Network Management
const NetworkMap = React.lazy(() => import('@/pages/network/NetworkMap'));
const Equipment = React.lazy(() => import('@/pages/network/Equipment'));
const Monitoring = React.lazy(() => import('@/pages/network/Monitoring'));
const Infrastructure = React.lazy(() => import('@/pages/network/Infrastructure'));

// Reports
const Reports = React.lazy(() => import('@/pages/reports/Reports'));
const Analytics = React.lazy(() => import('@/pages/reports/Analytics'));

// Settings
const Settings = React.lazy(() => import('@/pages/settings/Settings'));
const UserManagement = React.lazy(() => import('@/pages/settings/UserManagement'));
const SystemConfig = React.lazy(() => import('@/pages/settings/SystemConfig'));

// Tickets & Support
const Tickets = React.lazy(() => import('@/pages/support/Tickets'));
const TicketDetail = React.lazy(() => import('@/pages/support/TicketDetail'));

// Hooks
import { useAuth } from '@/hooks/useAuth';

// Types
interface AppProps {}

// Query Client Configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      refetchOnReconnect: 'always',
    },
    mutations: {
      retry: 1,
    },
  },
});

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  return <>{children}</>;
};

// Public Route Component (redirect if already authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

// Main App Component
const App: React.FC<AppProps> = () => {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={(error, errorInfo) => {
        console.error('Application Error:', error, errorInfo);
        // Send error to monitoring service (Sentry, etc.)
      }}
    >
      <HelmetProvider>
        <QueryClientProvider client={queryClient}>
          <ThemeProvider>
            <AuthProvider>
              <SettingsProvider>
                <Router>
                  <div className="App min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
                    <Suspense fallback={<LoadingSpinner />}>
                      <Routes>
                        {/* Public Authentication Routes */}
                        <Route
                          path="/auth/*"
                          element={
                            <PublicRoute>
                              <AuthLayout>
                                <Routes>
                                  <Route path="login" element={<Login />} />
                                  <Route path="register" element={<Register />} />
                                  <Route path="forgot-password" element={<ForgotPassword />} />
                                  <Route path="*" element={<Navigate to="/auth/login" replace />} />
                                </Routes>
                              </AuthLayout>
                            </PublicRoute>
                          }
                        />

                        {/* Protected Application Routes */}
                        <Route
                          path="/*"
                          element={
                            <ProtectedRoute>
                              <MainLayout>
                                <Routes>
                                  {/* Dashboard */}
                                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                                  <Route path="/dashboard" element={<Dashboard />} />

                                  {/* Customer Management */}
                                  <Route path="/customers" element={<Customers />} />
                                  <Route path="/customers/add" element={<AddCustomer />} />
                                  <Route path="/customers/:id" element={<CustomerDetail />} />

                                  {/* Billing & Invoicing */}
                                  <Route path="/billing/invoices" element={<Invoices />} />
                                  <Route path="/billing/invoices/create" element={<CreateInvoice />} />
                                  <Route path="/billing/invoices/:id" element={<InvoiceDetail />} />
                                  <Route path="/billing/payments" element={<Payments />} />

                                  {/* Network Management */}
                                  <Route path="/network/map" element={<NetworkMap />} />
                                  <Route path="/network/equipment" element={<Equipment />} />
                                  <Route path="/network/monitoring" element={<Monitoring />} />
                                  <Route path="/network/infrastructure" element={<Infrastructure />} />

                                  {/* Reports & Analytics */}
                                  <Route path="/reports" element={<Reports />} />
                                  <Route path="/reports/analytics" element={<Analytics />} />

                                  {/* Support & Tickets */}
                                  <Route path="/support/tickets" element={<Tickets />} />
                                  <Route path="/support/tickets/:id" element={<TicketDetail />} />

                                  {/* Settings */}
                                  <Route path="/settings" element={<Settings />} />
                                  <Route path="/settings/users" element={<UserManagement />} />
                                  <Route path="/settings/system" element={<SystemConfig />} />

                                  {/* 404 - Not Found */}
                                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                                </Routes>
                              </MainLayout>
                            </ProtectedRoute>
                          }
                        />
                      </Routes>
                    </Suspense>

                    {/* Global Toast Notifications */}
                    <Toaster
                      position="top-right"
                      reverseOrder={false}
                      gutter={8}
                      containerClassName=""
                      containerStyle={{}}
                      toastOptions={{
                        // Define default options
                        className: '',
                        duration: 4000,
                        style: {
                          background: '#363636',
                          color: '#fff',
                        },
                        // Default options for specific types
                        success: {
                          duration: 3000,
                          style: {
                            background: 'green',
                          },
                          iconTheme: {
                            primary: 'green',
                            secondary: 'black',
                          },
                        },
                        error: {
                          duration: 5000,
                          style: {
                            background: '#ff0000',
                          },
                        },
                      }}
                    />
                  </div>
                </Router>
              </SettingsProvider>
            </AuthProvider>
          </ThemeProvider>
          
          {/* Development Tools */}
          {process.env.NODE_ENV === 'development' && (
            <ReactQueryDevtools initialIsOpen={false} />
          )}
        </QueryClientProvider>
      </HelmetProvider>
    </ErrorBoundary>
  );
};

export default App;