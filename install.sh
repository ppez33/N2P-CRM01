#!/bin/bash

# =================================================================
# N2P-CRM01 - ISP Management System
# Automatic Installation Script for Linux
# =================================================================
# Author: Net2Point Engineering Team
# Repository: https://github.com/ppez33/N2P-CRM01
# License: Commercial
# =================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="N2P-CRM01"
VERSION="1.0.0"
INSTALL_DIR="/opt/n2p-crm01"
SERVICE_USER="n2p"
DATABASE_NAME="n2p_crm"
LOG_FILE="/tmp/n2p-install.log"

# System detection
OS=""
DISTRO=""
PACKAGE_MANAGER=""

# Functions
print_banner() {
    clear
    echo -e "${CYAN}"
    echo "================================================================="
    echo "  _   _ ____  ____       ____ ____  __  __  ___  _ "
    echo " | \ | |___ \|  _ \     / ___|  _ \|  \/  |/ _ \/ |"
    echo " |  \| | __) | |_) |   | |   | |_) | |\/| | | | | |"
    echo " | |\  |/ __/|  __/    | |___|  _ <| |  | | |_| | |"
    echo " |_| \_|_____|_|        \____|_| \_\_|  |_|\___/|_|"
    echo ""
    echo "        ISP Management System v${VERSION}"
    echo "     Automatic Installation Script for Linux"
    echo "================================================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1" >> "$LOG_FILE"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1" >> "$LOG_FILE"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1" >> "$LOG_FILE"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$LOG_FILE"
    exit 1
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
    fi
}

# Detect operating system
detect_os() {
    print_step "Detecting operating system..."
    
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        DISTRO=$VERSION_ID
    elif [[ -f /etc/redhat-release ]]; then
        OS=$(cat /etc/redhat-release)
    elif [[ -f /etc/debian_version ]]; then
        OS="Debian"
        DISTRO=$(cat /etc/debian_version)
    else
        print_error "Cannot detect operating system"
    fi

    # Determine package manager
    if command -v apt-get &> /dev/null; then
        PACKAGE_MANAGER="apt"
    elif command -v yum &> /dev/null; then
        PACKAGE_MANAGER="yum"
    elif command -v dnf &> /dev/null; then
        PACKAGE_MANAGER="dnf"
    elif command -v zypper &> /dev/null; then
        PACKAGE_MANAGER="zypper"
    else
        print_error "Unsupported package manager"
    fi

    print_success "OS: $OS, Package Manager: $PACKAGE_MANAGER"
}

# Check system requirements
check_requirements() {
    print_step "Checking system requirements..."
    
    # Check CPU cores
    CPU_CORES=$(nproc)
    if [[ $CPU_CORES -lt 2 ]]; then
        print_warning "Minimum 4 CPU cores recommended (found: $CPU_CORES)"
    fi

    # Check RAM
    RAM_GB=$(($(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 / 1024))
    if [[ $RAM_GB -lt 8 ]]; then
        print_warning "Minimum 8GB RAM recommended (found: ${RAM_GB}GB)"
    fi

    # Check disk space
    DISK_AVAILABLE=$(df / | tail -1 | awk '{print $4}')
    DISK_GB=$((DISK_AVAILABLE / 1024 / 1024))
    if [[ $DISK_GB -lt 50 ]]; then
        print_error "Minimum 50GB disk space required (available: ${DISK_GB}GB)"
    fi

    print_success "System requirements check passed"
}

# Update system
update_system() {
    print_step "Updating system packages..."
    
    case $PACKAGE_MANAGER in
        apt)
            export DEBIAN_FRONTEND=noninteractive
            apt-get update -y
            apt-get upgrade -y
            apt-get install -y curl wget gnupg2 software-properties-common apt-transport-https ca-certificates lsb-release
            ;;
        yum)
            yum update -y
            yum install -y curl wget gnupg2 epel-release
            ;;
        dnf)
            dnf update -y
            dnf install -y curl wget gnupg2
            ;;
    esac
    
    print_success "System updated"
}

# Install Docker
install_docker() {
    print_step "Installing Docker..."
    
    if command -v docker &> /dev/null; then
        print_success "Docker already installed"
        return
    fi

    case $PACKAGE_MANAGER in
        apt)
            # Add Docker's official GPG key
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
            
            # Add Docker repository
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
            
            # Install Docker
            apt-get update -y
            apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
            ;;
        yum|dnf)
            # Add Docker repository
            $PACKAGE_MANAGER config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            
            # Install Docker
            $PACKAGE_MANAGER install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
            ;;
    esac

    # Start and enable Docker
    systemctl start docker
    systemctl enable docker
    
    # Add user to docker group
    usermod -aG docker $SERVICE_USER 2>/dev/null || true
    
    print_success "Docker installed and configured"
}

# Install Docker Compose
install_docker_compose() {
    print_step "Installing Docker Compose..."
    
    if command -v docker-compose &> /dev/null; then
        print_success "Docker Compose already installed"
        return
    fi

    # Download Docker Compose
    COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    # Make executable
    chmod +x /usr/local/bin/docker-compose
    
    # Create symlink
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    print_success "Docker Compose installed"
}

# Install Python
install_python() {
    print_step "Installing Python 3.11+..."
    
    case $PACKAGE_MANAGER in
        apt)
            add-apt-repository -y ppa:deadsnakes/ppa
            apt-get update -y
            apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
            
            # Set Python 3.11 as default
            update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
            ;;
        yum|dnf)
            $PACKAGE_MANAGER install -y python3.11 python3.11-pip python3.11-devel
            ;;
    esac
    
    print_success "Python installed"
}

# Install Node.js
install_nodejs() {
    print_step "Installing Node.js 18+..."
    
    # Install NodeSource repository
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    
    case $PACKAGE_MANAGER in
        apt)
            apt-get install -y nodejs
            ;;
        yum|dnf)
            $PACKAGE_MANAGER install -y nodejs npm
            ;;
    esac
    
    print_success "Node.js installed"
}

# Create system user
create_user() {
    print_step "Creating system user..."
    
    if id "$SERVICE_USER" &>/dev/null; then
        print_success "User $SERVICE_USER already exists"
    else
        useradd -r -m -s /bin/bash "$SERVICE_USER"
        usermod -aG docker "$SERVICE_USER"
        print_success "User $SERVICE_USER created"
    fi
}

# Create directories
create_directories() {
    print_step "Creating directories..."
    
    mkdir -p "$INSTALL_DIR"
    mkdir -p /var/log/n2p-crm01
    mkdir -p /var/lib/n2p-crm01
    mkdir -p /etc/n2p-crm01
    
    chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
    chown -R "$SERVICE_USER:$SERVICE_USER" /var/log/n2p-crm01
    chown -R "$SERVICE_USER:$SERVICE_USER" /var/lib/n2p-crm01
    chown -R "$SERVICE_USER:$SERVICE_USER" /etc/n2p-crm01
    
    print_success "Directories created"
}

# Download application
download_application() {
    print_step "Downloading N2P-CRM01..."
    
    cd "$INSTALL_DIR"
    
    if [[ -d .git ]]; then
        # Update existing installation
        print_info "Updating existing installation..."
        sudo -u "$SERVICE_USER" git pull
    else
        # Fresh installation
        print_info "Downloading from repository..."
        sudo -u "$SERVICE_USER" git clone https://github.com/ppez33/N2P-CRM01.git .
    fi
    
    chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
    print_success "Application downloaded"
}

# Configure environment
configure_environment() {
    print_step "Configuring environment..."
    
    cd "$INSTALL_DIR"
    
    # Copy environment file if it doesn't exist
    if [[ ! -f .env ]]; then
        cp .env.example .env
        
        # Generate secure keys
        SECRET_KEY=$(openssl rand -hex 32)
        JWT_SECRET=$(openssl rand -hex 32)
        
        # Update .env file
        sed -i "s/your-super-secret-key-change-this-in-production-min-32-chars/$SECRET_KEY/" .env
        sed -i "s/your-jwt-secret-key-change-this/$JWT_SECRET/" .env
        
        chown "$SERVICE_USER:$SERVICE_USER" .env
        chmod 600 .env
        
        print_success "Environment configured"
        print_warning "Please edit /opt/n2p-crm01/.env and configure your API keys!"
    else
        print_success "Environment file already exists"
    fi
}

# Install dependencies
install_dependencies() {
    print_step "Installing application dependencies..."
    
    cd "$INSTALL_DIR"
    
    # Backend dependencies
    if [[ -f backend/requirements.txt ]]; then
        print_info "Installing Python dependencies..."
        sudo -u "$SERVICE_USER" python3 -m venv backend/venv
        sudo -u "$SERVICE_USER" bash -c "source backend/venv/bin/activate && pip install --upgrade pip && pip install -r backend/requirements.txt"
    fi
    
    # Frontend dependencies
    if [[ -f frontend/package.json ]]; then
        print_info "Installing Node.js dependencies..."
        cd frontend
        sudo -u "$SERVICE_USER" npm install
        cd ..
    fi
    
    print_success "Dependencies installed"
}

# Setup systemd services
setup_services() {
    print_step "Setting up systemd services..."
    
    # N2P-CRM01 Backend Service
    cat > /etc/systemd/system/n2p-crm01.service << EOF
[Unit]
Description=N2P-CRM01 ISP Management System
After=network.target
Requires=docker.service
After=docker.service

[Service]
Type=forking
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Enable and start service
    systemctl daemon-reload
    systemctl enable n2p-crm01
    
    print_success "Systemd services configured"
}

# Configure firewall
configure_firewall() {
    print_step "Configuring firewall..."
    
    if command -v ufw &> /dev/null; then
        # Ubuntu/Debian firewall
        ufw allow 22/tcp    # SSH
        ufw allow 80/tcp    # HTTP
        ufw allow 443/tcp   # HTTPS
        ufw allow 8000/tcp  # API
        ufw --force enable
    elif command -v firewall-cmd &> /dev/null; then
        # CentOS/RHEL firewall
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --permanent --add-port=8000/tcp
        firewall-cmd --reload
    fi
    
    print_success "Firewall configured"
}

# Start application
start_application() {
    print_step "Starting N2P-CRM01..."
    
    cd "$INSTALL_DIR"
    
    # Start with Docker Compose
    sudo -u "$SERVICE_USER" docker-compose up -d
    
    # Wait for services to start
    sleep 30
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "N2P-CRM01 started successfully"
    else
        print_error "Failed to start N2P-CRM01"
    fi
}

# Generate admin credentials
generate_admin_credentials() {
    print_step "Generating admin credentials..."
    
    ADMIN_PASSWORD=$(openssl rand -base64 12)
    
    cat > "$INSTALL_DIR/admin_credentials.txt" << EOF
=================================================================
N2P-CRM01 - Initial Admin Credentials
=================================================================
Created: $(date)

URL: http://$(hostname -I | awk '{print $1}')
Admin User: admin
Admin Password: $ADMIN_PASSWORD

IMPORTANT: Change this password after first login!

API Documentation: http://$(hostname -I | awk '{print $1}'):8000/docs
=================================================================
EOF

    chown "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR/admin_credentials.txt"
    chmod 600 "$INSTALL_DIR/admin_credentials.txt"
    
    print_success "Admin credentials generated"
}

# Main installation function
main() {
    print_banner
    
    # Pre-installation checks
    check_root
    detect_os
    check_requirements
    
    # System preparation
    update_system
    create_user
    create_directories
    
    # Install components
    install_docker
    install_docker_compose
    install_python
    install_nodejs
    
    # Application setup
    download_application
    configure_environment
    install_dependencies
    
    # System configuration
    setup_services
    configure_firewall
    
    # Start application
    start_application
    generate_admin_credentials
    
    # Final message
    echo -e "${GREEN}"
    echo "================================================================="
    echo "           🎉 N2P-CRM01 Installation Complete! 🎉"
    echo "================================================================="
    echo ""
    echo "✅ Application URL: http://$(hostname -I | awk '{print $1}')"
    echo "✅ API Documentation: http://$(hostname -I | awk '{print $1}'):8000/docs"
    echo "✅ Admin credentials: $INSTALL_DIR/admin_credentials.txt"
    echo ""
    echo "📁 Installation directory: $INSTALL_DIR"
    echo "📋 Logs: /var/log/n2p-crm01"
    echo "⚙️  Configuration: $INSTALL_DIR/.env"
    echo ""
    echo "🔧 Next steps:"
    echo "   1. Edit $INSTALL_DIR/.env with your API keys"
    echo "   2. Restart: systemctl restart n2p-crm01"
    echo "   3. View logs: docker-compose logs -f"
    echo ""
    echo "📖 Documentation: https://github.com/ppez33/N2P-CRM01"
    echo "💬 Support: Discord, GitHub Issues"
    echo "================================================================="
    echo -e "${NC}"
}

# Error handling
trap 'print_error "Installation failed. Check log: $LOG_FILE"' ERR

# Run main installation
main "$@"