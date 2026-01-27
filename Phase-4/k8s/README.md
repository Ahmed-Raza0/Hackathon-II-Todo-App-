# Kubernetes Deployment for Todo App (Phase IV)

This directory contains the Kubernetes deployment configuration for the Todo application using Helm charts.

## Prerequisites

- Docker
- Minikube
- kubectl
- Helm 3+

## Deployment Steps

1. Start Minikube:
   ```bash
   minikube start --driver=docker
   ```

2. Create the namespace:
   ```bash
   kubectl create namespace todo-phase4
   ```

3. Build Docker images:
   ```bash
   # Build backend image
   docker build -t todo-backend:phase4 backend/.

   # Build frontend image
   docker build -t todo-frontend:phase4 frontend/.
   ```

4. Load images into Minikube:
   ```bash
   minikube image load todo-backend:phase4
   minikube image load todo-frontend:phase4
   ```

5. Deploy using Helm:
   ```bash
   # Deploy backend first
   cccc

   # Deploy frontend
   helm install frontend k8s/helm/frontend --namespace todo-phase4 --set image.repository=todo-frontend,image.tag=phase4
   ```

6. Access the application:
   ```bash
   minikube service frontend-service --namespace todo-phase4
   ```

## Fallback Procedures

If AI tools are unavailable:
- Use manual Docker CLI and kubectl apply for deployments
- Manually create Kubernetes resources using kubectl create -f <manifest-file>
- Monitor deployments with kubectl get pods, kubectl logs, etc.

## Configuration

- The backend expects database connection details via Kubernetes secrets
- Frontend connects to backend via internal service: `http://backend-service.todo-phase4.svc.cluster.local:8000`
- All sensitive data (database URLs, secrets) are stored in Kubernetes secrets

## Cleanup

To remove all resources:
```bash
helm uninstall frontend backend --namespace todo-phase4
kubectl delete namespace todo-phase4
```