# 📁 N2P-CRM01 - Estructura del Proyecto

Esta documentación describe la estructura completa del repositorio N2P-CRM01.

## 🏗️ **Estructura de Directorios**

```
N2P-CRM01/
├── 📄 README.md                    # Documentación principal
├── 📄 LICENSE                      # Licencia comercial
├── 📄 .gitignore                   # Archivos excluidos
├── 📄 .env.example                 # Variables de entorno template
├── 📄 docker-compose.yml           # Orchestración de contenedores
├── 📄 docker-compose.prod.yml      # Producción con Docker
├── 🔧 install.sh                   # Instalador Linux/macOS
├── 🔧 install.bat                  # Instalador Windows
├── 📄 STRUCTURE.md                 # Este archivo
│
├── 📂 backend/                     # FastAPI Backend
│   ├── 📄 main.py                  # Aplicación principal
│   ├── 📄 requirements.txt         # Dependencias Python
│   ├── 📄 Dockerfile               # Container backend
│   ├── 📄 pytest.ini               # Configuración de tests
│   ├── 📄 alembic.ini               # Migraciones de DB
│   │
│   ├── 📂 app/                     # Código de aplicación
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py               # FastAPI app
│   │   ├── 📄 dependencies.py       # Dependencias globales
│   │   │
│   │   ├── 📂 api/                 # Rutas API
│   │   │   ├── 📂 v1/              # API versión 1
│   │   │   │   ├── 📄 router.py     # Router principal v1
│   │   │   │   ├── 📂 clients/      # Gestión de clientes
│   │   │   │   ├── 📂 billing/      # Facturación
│   │   │   │   ├── 📂 network/      # Red y equipos
│   │   │   │   ├── 📂 monitoring/   # Monitoreo
│   │   │   │   └── 📂 reports/      # Reportes
│   │   │   ├── 📂 auth/            # Autenticación
│   │   │   └── 📂 health/          # Health checks
│   │   │
│   │   ├── 📂 core/                # Núcleo del sistema
│   │   │   ├── 📄 config.py         # Configuración
│   │   │   ├── 📄 database.py       # Conexión DB
│   │   │   ├── 📄 redis_client.py   # Cliente Redis
│   │   │   ├── 📄 security.py       # Seguridad/JWT
│   │   │   ├── 📄 logging_config.py # Logging
│   │   │   └── 📄 exceptions.py     # Excepciones
│   │   │
│   │   ├── 📂 models/              # Modelos de datos
│   │   │   ├── 📄 user.py          # Usuario
│   │   │   ├── 📄 customer.py      # Cliente
│   │   │   ├── 📄 invoice.py       # Factura
│   │   │   ├── 📄 network.py       # Red/Equipos
│   │   │   └── 📄 monitoring.py    # Monitoreo
│   │   │
│   │   ├── 📂 services/            # Lógica de negocio
│   │   │   ├── 📂 mikrotik/        # Integración Mikrotik
│   │   │   ├── 📂 powerchat/       # WhatsApp/SMS
│   │   │   ├── 📂 bequant/         # QoE Optimization
│   │   │   ├── 📂 ai_monitoring/   # IA Predictiva
│   │   │   ├── 📂 billing/         # Sistema de facturación
│   │   │   └── 📂 gis/             # Mapeo/GIS
│   │   │
│   │   ├── 📂 middleware/          # Middlewares
│   │   │   ├── 📄 rate_limiting.py # Rate limiting
│   │   │   ├── 📄 security.py      # Headers seguridad
│   │   │   └── 📄 request_logging.py # Log requests
│   │   │
│   │   └── 📂 utils/               # Utilidades
│   │       ├── 📄 validators.py     # Validadores
│   │       ├── 📄 helpers.py        # Funciones útiles
│   │       ├── 📄 email.py          # Email utilities
│   │       └── 📄 encryption.py     # Cifrado
│   │
│   ├── 📂 alembic/                 # Migraciones DB
│   │   ├── 📂 versions/            # Versiones migración
│   │   └── 📄 env.py               # Configuración Alembic
│   │
│   ├── 📂 static/                  # Archivos estáticos
│   │   ├── 📂 images/              # Imágenes
│   │   ├── 📂 templates/           # Templates email
│   │   └── 📂 uploads/             # Archivos subidos
│   │
│   └── 📂 logs/                    # Archivos de log
│       ├── 📄 app.log              # Log aplicación
│       ├── 📄 error.log            # Log errores
│       └── 📄 access.log           # Log acceso
│
├── 📂 frontend/                    # React Frontend
│   ├── 📄 package.json             # Dependencias Node.js
│   ├── 📄 tsconfig.json            # Configuración TypeScript
│   ├── 📄 vite.config.ts           # Configuración Vite
│   ├── 📄 tailwind.config.js       # Configuración Tailwind
│   ├── 📄 Dockerfile               # Container frontend
│   ├── 📄 nginx.conf               # Configuración Nginx
│   │
│   ├── 📂 public/                  # Archivos públicos
│   │   ├── 📄 index.html           # HTML principal
│   │   ├── 📄 favicon.ico          # Favicon
│   │   └── 📂 icons/               # Iconos PWA
│   │
│   ├── 📂 src/                     # Código fuente
│   │   ├── 📄 main.tsx             # Entrada principal
│   │   ├── 📄 App.tsx              # Componente principal
│   │   ├── 📄 index.css            # Estilos globales
│   │   ├── 📄 vite-env.d.ts        # Types Vite
│   │   │
│   │   ├── 📂 components/          # Componentes React
│   │   │   ├── 📂 common/          # Componentes comunes
│   │   │   │   ├── 📄 Button.tsx    # Botón reutilizable
│   │   │   │   ├── 📄 Input.tsx     # Input reutilizable
│   │   │   │   ├── 📄 Modal.tsx     # Modal/Dialog
│   │   │   │   ├── 📄 LoadingSpinner.tsx # Spinner carga
│   │   │   │   └── 📄 ErrorBoundary.tsx # Error boundary
│   │   │   │
│   │   │   ├── 📂 layout/          # Layout components
│   │   │   │   ├── 📄 MainLayout.tsx # Layout principal
│   │   │   │   ├── 📄 Sidebar.tsx   # Barra lateral
│   │   │   │   ├── 📄 Header.tsx    # Cabecera
│   │   │   │   └── 📄 Footer.tsx    # Pie de página
│   │   │   │
│   │   │   ├── 📂 dashboard/       # Dashboard
│   │   │   ├── 📂 clients/         # Gestión clientes
│   │   │   ├── 📂 billing/         # Facturación
│   │   │   ├── 📂 network/         # Red y monitoreo
│   │   │   └── 📂 reports/         # Reportes
│   │   │
│   │   ├── 📂 pages/               # Páginas/Vistas
│   │   │   ├── 📂 auth/            # Autenticación
│   │   │   │   ├── 📄 Login.tsx     # Página login
│   │   │   │   ├── 📄 Register.tsx  # Registro
│   │   │   │   └── 📄 ForgotPassword.tsx
│   │   │   │
│   │   │   ├── 📂 dashboard/       # Dashboard
│   │   │   │   └── 📄 Dashboard.tsx # Vista principal
│   │   │   │
│   │   │   ├── 📂 clients/         # Clientes
│   │   │   │   ├── 📄 Customers.tsx # Lista clientes
│   │   │   │   ├── 📄 CustomerDetail.tsx # Detalle
│   │   │   │   └── 📄 AddCustomer.tsx # Alta cliente
│   │   │   │
│   │   │   ├── 📂 billing/         # Facturación
│   │   │   ├── 📂 network/         # Red
│   │   │   ├── 📂 reports/         # Reportes
│   │   │   └── 📂 settings/        # Configuración
│   │   │
│   │   ├── 📂 hooks/               # React Hooks
│   │   │   ├── 📄 useAuth.ts        # Hook autenticación
│   │   │   ├── 📄 useApi.ts         # Hook API calls
│   │   │   ├── 📄 useLocalStorage.ts # Hook localStorage
│   │   │   └── 📄 useWebSocket.ts   # Hook WebSocket
│   │   │
│   │   ├── 📂 services/            # Servicios API
│   │   │   ├── 📄 api.ts            # Cliente API base
│   │   │   ├── 📄 auth.ts           # Servicio auth
│   │   │   ├── 📄 customers.ts      # Servicio clientes
│   │   │   ├── 📄 billing.ts        # Servicio facturación
│   │   │   └── 📄 network.ts        # Servicio red
│   │   │
│   │   ├── 📂 store/               # Estado global
│   │   │   ├── 📄 authStore.ts      # Store autenticación
│   │   │   ├── 📄 customerStore.ts  # Store clientes
│   │   │   └── 📄 appStore.ts       # Store aplicación
│   │   │
│   │   ├── 📂 utils/               # Utilidades
│   │   │   ├── 📄 constants.ts      # Constantes
│   │   │   ├── 📄 formatters.ts     # Formateadores
│   │   │   ├── 📄 validators.ts     # Validadores
│   │   │   └── 📄 helpers.ts        # Funciones útiles
│   │   │
│   │   ├── 📂 types/               # Tipos TypeScript
│   │   │   ├── 📄 auth.ts           # Tipos autenticación
│   │   │   ├── 📄 customer.ts       # Tipos cliente
│   │   │   ├── 📄 api.ts            # Tipos API
│   │   │   └── 📄 common.ts         # Tipos comunes
│   │   │
│   │   ├── 📂 styles/              # Estilos
│   │   │   ├── 📄 globals.css       # Estilos globales
│   │   │   ├── 📄 components.css    # Estilos componentes
│   │   │   └── 📂 themes/           # Temas
│   │   │
│   │   └── 📂 assets/              # Assets estáticos
│   │       ├── 📂 images/          # Imágenes
│   │       ├── 📂 icons/           # Iconos
│   │       └── 📂 fonts/           # Fuentes
│   │
│   └── 📂 dist/                    # Build de producción
│
├── 📂 database/                    # Base de Datos
│   ├── 📂 schemas/                 # Esquemas DB
│   │   ├── 📄 mongodb_schema.js     # Esquema MongoDB
│   │   └── 📄 postgresql_schema.sql # Esquema PostgreSQL
│   │
│   ├── 📂 seeds/                   # Datos iniciales
│   │   ├── 📄 admin_user.json       # Usuario admin
│   │   ├── 📄 sample_customers.json # Clientes ejemplo
│   │   └── 📄 default_settings.json # Configuración
│   │
│   ├── 📂 migrations/              # Migraciones
│   │   ├── 📄 001_initial.py        # Migración inicial
│   │   └── 📄 002_add_ai_tables.py  # Tablas IA
│   │
│   └── 📂 backup/                  # Respaldos
│       ├── 📄 backup_script.sh      # Script backup
│       └── 📄 restore_script.sh     # Script restore
│
├── 📂 docker/                      # Docker configs
│   ├── 📂 development/             # Desarrollo
│   │   ├── 📄 docker-compose.dev.yml
│   │   └── 📄 .env.dev
│   │
│   └── 📂 production/              # Producción
│       ├── 📄 docker-compose.prod.yml
│       ├── 📄 .env.prod.example
│       └── 📄 nginx.prod.conf
│
├── 📂 scripts/                     # Scripts utilidades
│   ├── 📂 install/                 # Instalación
│   │   ├── 📄 ubuntu_install.sh     # Ubuntu/Debian
│   │   ├── 📄 centos_install.sh     # CentOS/RHEL
│   │   └── 📄 windows_install.ps1   # Windows PowerShell
│   │
│   ├── 📂 deploy/                  # Despliegue
│   │   ├── 📄 deploy_staging.sh     # Deploy staging
│   │   ├── 📄 deploy_production.sh  # Deploy producción
│   │   └── 📄 rollback.sh           # Rollback
│   │
│   ├── 📂 backup/                  # Respaldos
│   │   ├── 📄 daily_backup.sh       # Backup diario
│   │   ├── 📄 s3_backup.sh          # Backup a S3
│   │   └── 📄 Dockerfile            # Container backup
│   │
│   └── 📂 maintenance/             # Mantenimiento
│       ├── 📄 cleanup_logs.sh       # Limpiar logs
│       ├── 📄 update_system.sh      # Actualizar sistema
│       └── 📄 health_check.sh       # Health check
│
├── 📂 config/                      # Configuraciones
│   ├── 📂 nginx/                   # Nginx
│   │   ├── 📄 nginx.conf            # Configuración principal
│   │   ├── 📄 sites-available/      # Sites disponibles
│   │   └── 📄 ssl/                  # Certificados SSL
│   │
│   ├── 📂 systemd/                 # Servicios systemd
│   │   ├── 📄 n2p-backend.service   # Servicio backend
│   │   └── 📄 n2p-frontend.service  # Servicio frontend
│   │
│   ├── 📂 prometheus/              # Monitoreo
│   │   ├── 📄 prometheus.yml        # Config Prometheus
│   │   └── 📄 alert_rules.yml       # Reglas alertas
│   │
│   └── 📂 grafana/                 # Dashboards
│       ├── 📄 dashboard.json        # Dashboard principal
│       └── 📄 datasources.yml       # Fuentes datos
│
├── 📂 docs/                        # Documentación
│   ├── 📄 installation.md          # Guía instalación
│   ├── 📄 user_guide.md            # Manual usuario
│   ├── 📄 developer_guide.md       # Guía desarrollador
│   ├── 📄 api_reference.md         # Referencia API
│   │
│   ├── 📂 screenshots/             # Capturas pantalla
│   ├── 📂 architecture/            # Diagramas arquitectura
│   └── 📂 tutorials/               # Tutoriales
│
├── 📂 tests/                       # Tests
│   ├── 📂 backend/                 # Tests backend
│   │   ├── 📂 unit/                # Tests unitarios
│   │   ├── 📂 integration/         # Tests integración
│   │   └── 📄 conftest.py           # Configuración pytest
│   │
│   ├── 📂 frontend/                # Tests frontend
│   │   ├── 📂 components/          # Tests componentes
│   │   ├── 📂 pages/               # Tests páginas
│   │   └── 📄 setup.ts             # Setup tests
│   │
│   └── 📂 e2e/                     # Tests end-to-end
│       ├── 📂 cypress/             # Tests Cypress
│       └── 📂 playwright/          # Tests Playwright
│
└── 📂 static/                      # Assets estáticos
    ├── 📂 images/                  # Imágenes globales
    │   ├── 📄 logo.png              # Logo aplicación
    │   ├── 📄 favicon.ico           # Favicon
    │   └── 📂 screenshots/          # Capturas
    │
    ├── 📂 icons/                   # Iconos
    │   ├── 📂 equipment/            # Iconos equipos
    │   └── 📂 status/               # Iconos estado
    │
    ├── 📂 templates/               # Templates
    │   ├── 📂 email/                # Templates email
    │   ├── 📂 pdf/                  # Templates PDF
    │   └── 📂 reports/              # Templates reportes
    │
    └── 📂 maps/                    # Mapas y GIS
        ├── 📂 kmz/                  # Archivos KMZ
        ├── 📂 layers/               # Capas mapas
        └── 📄 network_topology.json # Topología red
```

## 🚀 **Comandos de Desarrollo**

### **Inicio Rápido**

```bash
# Clonar repositorio
git clone https://github.com/ppez33/N2P-CRM01.git
cd N2P-CRM01

# Opción 1: Docker Compose (Recomendado)
cp .env.example .env
# Editar .env con tus configuraciones
docker-compose up -d

# Opción 2: Instalación manual
chmod +x install.sh
sudo ./install.sh
```

### **Desarrollo Local**

```bash
# Backend (Terminal 1)
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend
npm install
npm run dev  # http://localhost:3000

# Base de datos (Terminal 3)
docker run -d --name mongodb -p 27017:27017 mongo:6.0
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### **Tests**

```bash
# Backend tests
cd backend
python -m pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
npm run test:coverage

# E2E tests
npm run test:e2e
```

### **Build y Deploy**

```bash
# Build producción
docker build -t n2p-crm01:latest .
docker-compose -f docker-compose.prod.yml up -d

# Deploy staging
./scripts/deploy/deploy_staging.sh

# Deploy producción
./scripts/deploy/deploy_production.sh
```

## 🔧 **Configuración por Entorno**

### **Desarrollo**
- Base de datos: Local MongoDB/PostgreSQL
- Frontend: Vite dev server (HMR)
- Backend: Uvicorn con reload
- Debug: Habilitado
- Logs: Nivel DEBUG

### **Staging**
- Base de datos: Docker containers
- Build: Optimized builds
- Logs: Nivel INFO
- Monitoreo: Básico
- SSL: Self-signed certs

### **Producción**
- Base de datos: Cluster MongoDB/PostgreSQL
- CDN: Assets servidos desde CDN
- Load balancer: Nginx/HAProxy
- Monitoreo: Prometheus + Grafana
- SSL: Let's Encrypt/Commercial certs
- Logs: Centralizados (ELK Stack)
- Backup: Automatizado diario

## 📦 **Dependencias Principales**

### **Backend**
- **FastAPI**: Framework web async
- **Motor**: Driver MongoDB async
- **Redis**: Cache y sesiones
- **Celery**: Tasks background
- **SQLAlchemy**: ORM (si se usa PostgreSQL)
- **Pydantic**: Validación datos
- **Scikit-learn**: Machine Learning
- **Paramiko**: SSH para equipos red

### **Frontend**
- **React 18**: Framework UI
- **TypeScript**: Tipado estático
- **Vite**: Build tool
- **TailwindCSS**: Framework CSS
- **React Query**: State server
- **Zustand**: State management
- **React Router**: Routing
- **Recharts**: Gráficos
- **Leaflet**: Mapas

### **DevOps**
- **Docker**: Containerización
- **Nginx**: Proxy reverso
- **Prometheus**: Métricas
- **Grafana**: Dashboards
- **GitHub Actions**: CI/CD

## 🌟 **Características Principales**

### **✅ Implementado**
- [x] Estructura básica del proyecto
- [x] Configuración Docker
- [x] Sistema de autenticación
- [x] CRUD básico clientes
- [x] Integración Mikrotik básica
- [x] Dashboard principal
- [x] Sistema de logs

### **🚧 En Desarrollo**
- [ ] IA Monitoreo predictivo
- [ ] Integración Bequant QoE
- [ ] Mapeo GIS completo
- [ ] Facturación CFDI 4.0
- [ ] Notificaciones WhatsApp
- [ ] Reportes avanzados

### **📋 Roadmap**
- [ ] OLT Huawei/Vsol integration
- [ ] Mobile app (React Native)
- [ ] Multi-tenant support
- [ ] Advanced analytics
- [ ] Inventory management
- [ ] Customer portal

## 👥 **Contribuir**

1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Add: nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📞 **Soporte**

- **GitHub Issues**: [Issues](https://github.com/ppez33/N2P-CRM01/issues)
- **Email**: support@net2point.com
- **Discord**: [Net2Point Community](https://discord.gg/net2point)

---

**Desarrollado con ❤️ por Net2Point Engineering Team**  
**Cancún, Quintana Roo, México 🇲🇽**