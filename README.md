# Helm-Ayi: FastAPI + MySQL con ArgoCD

Este proyecto implementa una aplicación FastAPI con base de datos MySQL, desplegada en Kubernetes usando Helm charts y gestionada con ArgoCD.

## 🏗️ Arquitectura

- **Frontend**: FastAPI (Python)
- **Base de Datos**: MySQL 8
- **Orquestación**: Kubernetes
- **Gestión de Configuración**: Helm Charts
- **GitOps**: ArgoCD

## 📁 Estructura del Proyecto

```
helm-ayi/
├── instalador.ps1              # Script de instalación principal
├── argocd-apps/                # Aplicaciones de ArgoCD
│   ├── argocdpython.yaml       # App Python FastAPI
│   └── argocdmysql.yaml        # App MySQL
├── helm/                       # Charts de Helm
│   ├── python-chart/           # Chart para la app Python
│   └── mysql-chart/            # Chart para MySQL
├── k8s/                        # Manifests de Kubernetes
│   ├── fastapi/                # Manifests de FastAPI
│   └── mysql/                  # Manifests de MySQL
├── main.py                     # Aplicación FastAPI
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Imagen Docker
└── README.md                   # Este archivo
```

## 🚀 Instalación Rápida

### Prerrequisitos

- Kubernetes cluster (Docker Desktop, Minikube, etc.)
- kubectl configurado
- Helm instalado
- PowerShell (Windows)

### Despliegue Automático

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/rijmjada/helm-ayi.git
   cd helm-ayi
   ```

2. **Ejecutar el script de instalación:**
   ```powershell
   .\instalador.ps1
   ```

3. **Acceder a las aplicaciones:**
   - **ArgoCD**: https://localhost:8080 (admin / contraseña generada)
   - **FastAPI**: http://localhost:8000

## 📋 Endpoints de la API

### Crear datos de prueba
```bash
POST http://localhost:8000/crear
```

### Obtener clientes
```bash
GET http://localhost:8000/clientes
``` 