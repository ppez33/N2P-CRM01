# 🚀 N2P-CRM01 - ISP Management System

[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/net2point/N2P-CRM01)
[![License](https://img.shields.io/badge/license-Commercial-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org)
[![Docker](https://img.shields.io/badge/docker-supported-2496ed.svg)](https://docker.com)

**Sistema CRM/ERP avanzado para ISPs con IA, monitoreo predictivo, facturación automatizada y gestión de red completa.**

---

## 🌟 **Características Principales**

### 📊 **Dashboard Inteligente**
- **Métricas en tiempo real** de red y clientes
- **Alertas visuales** (Verde/Ámbar/Rojo)
- **KPIs automatizados** y reportes ejecutivos
- **Mapas interactivos** con Google Earth/KMZ

### 👥 **Gestión de Clientes**
- **Alta/Baja automatizada** con Mikrotik API
- **Suspensión automática** por vencimiento
- **Historial completo** de servicios y pagos
- **Notificaciones automáticas** vía Powerchat

### 💰 **Facturación Inteligente**
- **Facturación automática** CFDI 4.0 (México)
- **Múltiples métodos de pago**
- **Recordatorios automáticos**
- **Reportes fiscales** integrados

### 🌐 **Monitoreo de Red**
- **Mikrotik RouterOS v7+** integración completa
- **OLT Vsol/Huawei** soporte SSH/API
- **Calidad de Experiencia (QoE)** con Bequant
- **Mapas de red** con NAPs, fibra y clientes

### 🤖 **IA Predictiva**
- **Detección temprana** de fallos
- **Análisis de patrones** históricos
- **Escalamiento automático** L1/L2/L3
- **Optimización automática** de tráfico

### 📱 **Comunicaciones**
- **WhatsApp/SMS** automático vía Powerchat
- **Notificaciones** push y email
- **Tickets** de soporte integrados
- **Portal del cliente** autoservicio

---

## 🏗️ **Arquitectura Técnica**

```mermaid
graph TB
    A[React Frontend] --> B[FastAPI Backend]
    B --> C[MongoDB/PostgreSQL]
    B --> D[Redis Cache]
    B --> E[Mikrotik API]
    B --> F[Powerchat API]
    B --> G[Bequant QoE]
    B --> H[Google Maps API]
    I[AI/ML Models] --> B
    J[Background Tasks] --> B
```

### **Stack Tecnológico**
- **Frontend:** React 18+ TypeScript, Vite, TailwindCSS
- **Backend:** FastAPI, Python 3.11+, Pydantic
- **Database:** MongoDB 6.0+ o PostgreSQL 14+
- **Cache:** Redis 7.0+
- **Queue:** Celery + Redis
- **Proxy:** Nginx 1.20+
- **Container:** Docker + Docker Compose

---

## ⚡ **Instalación Rápida**

### **Opción 1: Docker Compose (Recomendado)**

```bash
# 1. Clonar repositorio
git clone https://github.com/net2point/N2P-CRM01.git
cd N2P-CRM01

# 2. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar configuración

# 3. Iniciar servicios
docker-compose up -d

# 4. Acceder a la aplicación
# http://localhost (Frontend)
# http://localhost:8000 (Backend API)
# Usuario: admin | Password: ver admin_credentials.txt
```

### **Opción 2: Script Automático Linux**

```bash
# Instalación en 1 comando
curl -fsSL https://raw.githubusercontent.com/net2point/N2P-CRM01/main/install.sh | sudo bash

# O manual
git clone https://github.com/net2point/N2P-CRM01.git
cd N2P-CRM01
sudo chmod +x install.sh
sudo ./install.sh
```

### **Opción 3: Script Windows**

```batch
REM Ejecutar como Administrador
git clone https://github.com/net2point/N2P-CRM01.git
cd N2P-CRM01
install.bat
```

---

## 📋 **Requisitos del Sistema**

### **Mínimos**
- **OS:** Ubuntu 20.04+ / Windows Server 2019+ / CentOS 8+
- **CPU:** 4 cores / 2.4 GHz
- **RAM:** 8GB
- **Storage:** 50GB SSD
- **Network:** 100 Mbps estable

### **Recomendados**
- **OS:** Ubuntu 22.04 LTS / Windows Server 2022
- **CPU:** 8 cores / 3.0 GHz
- **RAM:** 16GB+
- **Storage:** 200GB+ NVMe SSD
- **Network:** 1 Gbps dedicada

### **Software Requerido**
- **Python:** 3.11+
- **Node.js:** 18+
- **MongoDB:** 6.0+ o PostgreSQL 14+
- **Redis:** 7.0+
- **Docker:** 20.10+ (opcional)

---

## 🔧 **Configuración**

### **Variables de Entorno (.env)**

```bash
# Aplicación
APP_NAME=N2P-CRM01
DEBUG=false
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-change-this

# Base de Datos
MONGODB_URL=mongodb://localhost:27017/n2p_crm
# O PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/n2p_crm

# APIs Externas (CONFIGURAR OBLIGATORIO)
POWERCHAT_API_KEY=your-powerchat-api-key
POWERCHAT_API_URL=https://opentalk.wispcommunity.com/api/v1
BEQUANT_API_KEY=your-bequant-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Mikrotik (Configurar para cada router)
MIKROTIK_DEFAULT_PORT=8728
MIKROTIK_TIMEOUT=10

# Facturación
BILLING_CURRENCY=MXN
BILLING_TAX_RATE=0.16
AUTO_SUSPEND_DAYS=5
```

### **Configuración de Routers Mikrotik**

```bash
# En RouterOS, habilitar API
/ip service enable api
/ip service set api port=8728

# Crear usuario API
/user add name=n2p-api password=strong-password group=full
```

---

## 📖 **Documentación**

### **Enlaces Principales**
- **[📚 Documentación Completa](docs/)**
- **[🔌 API Reference](docs/api/)**
- **[🛠️ Guía de Instalación](docs/installation/)**
- **[👨‍💻 Guía de Desarrollo](docs/development/)**
- **[📋 Manual de Usuario](docs/user_guide/)**

### **Casos de Uso**
- **[🔌 Alta de Cliente](docs/use_cases/customer_registration.md)**
- **[💸 Suspensión por Pago](docs/use_cases/auto_suspension.md)**
- **[🚨 Monitoreo Predictivo](docs/use_cases/predictive_monitoring.md)**
- **[🗺️ Gestión de Red](docs/use_cases/network_management.md)**

---

## 🎯 **Casos de Uso Principales**

### **1. Alta de Cliente Automática**
1. Cliente se registra en portal web
2. Sistema crea perfil en CRM
3. Configura automáticamente Mikrotik (IP, queue, firewall)
4. Envía credenciales vía WhatsApp/SMS
5. Activa monitoreo y facturación

### **2. Corte de Fibra Inteligente**
1. IA detecta desconexión en NAPs
2. Identifica clientes afectados en mapa
3. Genera ticket automático
4. Notifica a técnicos y clientes
5. Bequant rebalancea tráfico restante

### **3. Facturación Automática**
1. Sistema genera facturas el día 1
2. Envía por email/WhatsApp automáticamente  
3. Procesa pagos recibidos
4. Día +5: suspende automáticamente morosos
5. Genera reportes ejecutivos

---

## 🧪 **Testing y Desarrollo**

### **Ejecutar Tests**

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests  
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### **Desarrollo Local**

```bash
# Backend (FastAPI)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (React)
cd frontend
npm install
npm run dev  # http://localhost:3000
```

---

## 🤝 **Contribuir**

### **Flujo de Desarrollo**
1. **Fork** el repositorio
2. **Crear** branch para feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Add: nueva funcionalidad'`)
4. **Push** al branch (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

### **Estándares de Código**
- **Python:** Black formatter, flake8 linter
- **JavaScript:** Prettier formatter, ESLint
- **Commits:** Conventional Commits format
- **Tests:** Cobertura mínima 80%

---

## 🐛 **Soporte y Bugs**

### **Reportar Problemas**
- **[🐛 GitHub Issues](https://github.com/net2point/N2P-CRM01/issues)**
- **[💬 Discord Community](https://discord.gg/net2point)**
- **[📧 Email Soporte](mailto:soporte@net2point.com)**

### **Recursos de Ayuda**
- **[📖 Knowledge Base](https://kb.net2point.com)**
- **[🎥 Video Tutorials](https://youtube.com/net2point)**
- **[📱 WhatsApp Support](https://wa.me/529984567890)**

---

## 📊 **Roadmap**

### **v1.1 (Q1 2025)**
- [x] Core CRM functionality
- [x] Mikrotik integration
- [x] Basic billing system
- [x] WhatsApp notifications

### **v1.2 (Q2 2025)**
- [ ] IA predictive monitoring
- [ ] Advanced reporting
- [ ] Mobile app (React Native)
- [ ] Multi-tenant support

### **v1.3 (Q3 2025)**
- [ ] OLT integration (Huawei/Vsol)
- [ ] Bequant QoE optimization
- [ ] Advanced GIS mapping
- [ ] Inventory management

---

## 📄 **Licencia**

Este proyecto está licenciado bajo términos comerciales. Ver [LICENSE](LICENSE) para más detalles.

### **Precios**
- **👥 Starter:** $99/mes (hasta 500 clientes)
- **🏢 Professional:** $299/mes (hasta 2,000 clientes)
- **🏭 Enterprise:** $799/mes (clientes ilimitados)
- **🏷️ White-label:** Contactar para cotización

### **Trial Gratuito**
**30 días gratis** - Sin limitaciones, sin tarjeta de crédito requerida.

---

## 🎉 **¡Comienza Ahora!**

```bash
# Instalación en 1 comando
curl -fsSL https://raw.githubusercontent.com/net2point/N2P-CRM01/main/install.sh | sudo bash

# O con Docker
git clone https://github.com/net2point/N2P-CRM01.git
cd N2P-CRM01
docker-compose up -d

# Accede a: http://localhost
```

**¡Transforma tu ISP con N2P-CRM01!** 🚀

---

**Desarrollado con ❤️ por Net2Point Engineering Team**  
**Cancún, Quintana Roo, México 🇲🇽**

[![Net2Point](https://img.shields.io/badge/Net2Point-Engineering-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMjIgMjJIMkwxMiAyWiIgZmlsbD0iIzAwRkZGRiIvPgo8L3N2Zz4K)](https://net2point.com)