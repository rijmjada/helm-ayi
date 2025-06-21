# Deploy-ArgoCD.ps1

# 1. Crear Namespace
kubectl create namespace argocd -o yaml --dry-run=client | kubectl apply -f -

# 2. Agregar el repo de Helm y actualizar
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# 3. Instalar Argo CD en el namespace
helm install argocd argo/argo-cd -n argocd

# 4. Esperar a que los pods estén listos
Write-Host "`nEsperando que los pods estén listos..."
kubectl wait --for=condition=available deploy/argocd-server -n argocd --timeout=180s

# 5. Aplicar las aplicaciones de Python y MySQL
Write-Host "`nAplicando aplicación de Python..."
kubectl apply -f argocd-apps/argocdpython.yaml

Write-Host "`nAplicando aplicación de MySQL..."
kubectl apply -f argocd-apps/argocdmysql.yaml

# 6. Hacer port-forward al servicio de Argo CD
Write-Host "`nIniciando port-forward en https://localhost:8080"
Start-Process powershell -ArgumentList "kubectl port-forward svc/argocd-server -n argocd 8080:443"

# 7. Esperar un poco para que las aplicaciones se sincronicen y luego hacer port-forward de Python
Write-Host "`nEsperando que las aplicaciones se sincronicen..."
Start-Sleep -Seconds 30

Write-Host "`nIniciando port-forward para la aplicación Python en http://localhost:8000"
Start-Process powershell -ArgumentList "kubectl port-forward service/simple-python 8000:8000 -n pythonns"

# 8. Obtener contraseña admin decodificada
Write-Host "`nObteniendo contraseña del usuario admin..."
$secret = kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}"
$password = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($secret))

Write-Host "`n======================="
Write-Host "🔐 Usuario: admin"
Write-Host "🔑 Contraseña: $password"
Write-Host "🌐 Acceso: https://localhost:8080"
Write-Host "======================="

Write-Host "`n✅ ArgoCD instalado y aplicaciones configuradas!"
Write-Host "🐍 Aplicación Python: pythonns-app"
Write-Host "🗄️  Aplicación MySQL: mysqlns-app"
Write-Host "`n🌐 URLs de acceso:"
Write-Host "   - ArgoCD: https://localhost:8080"
Write-Host "   - Python App: http://localhost:8000" 