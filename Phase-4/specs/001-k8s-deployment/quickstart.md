# Quickstart: Kubernetes Deployment (Phase IV)

## Prerequisites

- Docker Desktop installed and running
- Minikube installed and configured
- kubectl installed
- Helm installed
- Access to Neon PostgreSQL database (existing Phase III database)

## Setup Steps

### 1. Clone and Navigate to Repository
```bash
# Already in the repository root
cd /path/to/Hackathon-II-Todo-App
```

### 2. Start Minikube Cluster
```bash
minikube start
```

### 3. Create Dedicated Namespace
```bash
kubectl create namespace todo-phase4
```

### 4. Build Docker Images
```bash
# From repository root
cd frontend
docker build -t todo-frontend:phase4 .
cd ../backend
docker build -t todo-backend:phase4 .
```

### 5. Load Images into Minikube
```bash
# Load frontend image
minikube image load todo-frontend:phase4
# Load backend image
minikube image load todo-backend:phase4
```

### 6. Create Helm Charts
```bash
# Create frontend Helm chart
helm create k8s/helm/frontend
# Create backend Helm chart
helm create k8s/helm/backend
```

### 7. Configure Helm Charts
Update the Helm chart values.yaml files with:
- Image names and tags
- Resource requests and limits
- Environment variables
- Service configurations

### 8. Deploy Applications
```bash
# Deploy backend first
helm install backend k8s/helm/backend --namespace todo-phase4 --set image.repository=todo-backend,image.tag=phase4
# Deploy frontend
helm install frontend k8s/helm/frontend --namespace todo-phase4 --set image.repository=todo-frontend,image.tag=phase4
```

### 9. Verify Deployment
```bash
# Check pods
kubectl get pods -n todo-phase4
# Check services
kubectl get svc -n todo-phase4
# Access frontend
minikube service frontend -n todo-phase4
```

## Troubleshooting

### If Pods Fail to Start
1. Check logs: `kubectl logs <pod-name> -n todo-phase4`
2. Verify environment variables are set correctly
3. Confirm database connection settings

### If Services Are Not Accessible
1. Check service configuration: `kubectl describe svc <service-name> -n todo-phase4`
2. Verify NodePort assignment for frontend
3. Confirm backend service is accessible from frontend

### If Helm Installation Fails
1. Uninstall and retry: `helm uninstall <release-name> -n todo-phase4`
2. Validate chart syntax: `helm lint k8s/helm/<chart-name>`
3. Check image availability in Minikube

## Cleanup
```bash
# Uninstall Helm releases
helm uninstall frontend backend -n todo-phase4
# Stop Minikube
minikube stop
```