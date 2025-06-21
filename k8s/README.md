# Kubernetes Manifests

Esta carpeta contiene los manifiestos de Kubernetes organizados por componente siguiendo las mejores prácticas.

## 📁 Estructura

```
k8s/
├── mysql/                    # Componente MySQL
│   ├── namespace.yaml        # Namespace mysqlns
│   ├── secret.yaml          # Secret para contraseña root
│   ├── service.yaml         # Service headless para MySQL
│   └── statefulset.yaml     # StatefulSet con PVC
├── fastapi/                  # Componente FastAPI
│   ├── namespace.yaml        # Namespace pythonns
│   ├── configmap.yaml       # Configuración de la aplicación
│   ├── secret.yaml          # Secret para contraseña MySQL
│   ├── pv-pvc.yaml          # PersistentVolume y PVC
│   ├── deployment.yaml      # Deployment con 3 réplicas
│   └── service.yaml         # Service NodePort
└── README.md                # Este archivo
```

## 🚀 Despliegue

### Desplegar MySQL
```bash
# Aplicar todos los recursos de MySQL
kubectl apply -f k8s/mysql/

# O aplicar individualmente
kubectl apply -f k8s/mysql/namespace.yaml
kubectl apply -f k8s/mysql/secret.yaml
kubectl apply -f k8s/mysql/service.yaml
kubectl apply -f k8s/mysql/statefulset.yaml
```

### Desplegar FastAPI
```bash
# Aplicar todos los recursos de FastAPI
kubectl apply -f k8s/fastapi/

# O aplicar individualmente
kubectl apply -f k8s/fastapi/namespace.yaml
kubectl apply -f k8s/fastapi/configmap.yaml
kubectl apply -f k8s/fastapi/secret.yaml
kubectl apply -f k8s/fastapi/pv-pvc.yaml
kubectl apply -f k8s/fastapi/deployment.yaml
kubectl apply -f k8s/fastapi/service.yaml
```

### Desplegar Todo
```bash
# Desplegar ambos componentes
kubectl apply -f k8s/mysql/
kubectl apply -f k8s/fastapi/
```

## 🔍 Verificación

### Verificar Pods
```bash
kubectl get pods -n mysqlns
kubectl get pods -n pythonns
```

### Verificar Servicios
```bash
kubectl get svc -n mysqlns
kubectl get svc -n pythonns
```

### Verificar Storage
```bash
kubectl get pv,pvc -n pythonns
```

## 🧹 Limpieza

### Eliminar FastAPI
```bash
kubectl delete -f k8s/fastapi/
```

### Eliminar MySQL
```bash
kubectl delete -f k8s/mysql/
```

### Eliminar Todo
```bash
kubectl delete -f k8s/
```

## 📋 Ventajas de esta Estructura

- ✅ **Separación por componente**: Cada servicio tiene su propio directorio
- ✅ **Archivos pequeños**: Cada archivo tiene una responsabilidad específica
- ✅ **Fácil mantenimiento**: Cambios localizados por componente
- ✅ **Despliegue independiente**: Puedes desplegar componentes por separado
- ✅ **Escalabilidad**: Fácil agregar nuevos componentes
- ✅ **Preparado para Helm**: Estructura compatible con Helm charts
- ✅ **Control de versiones**: Mejor tracking de cambios
- ✅ **CI/CD friendly**: Fácil automatización
- ✅ **Nombres válidos**: Namespaces con nombres cortos y válidos

## 🔄 Migración desde la Estructura Anterior

La estructura anterior (`yamls/`) se mantiene para compatibilidad, pero se recomienda usar la nueva estructura (`k8s/`) para futuros despliegues.

## 🏷️ Nombres de Namespaces

- **`mysqlns`**: Contiene todos los recursos relacionados con la base de datos MySQL
- **`pythonns`**: Contiene todos los recursos de la aplicación FastAPI 