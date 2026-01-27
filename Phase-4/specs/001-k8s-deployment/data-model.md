# Data Model: Kubernetes Deployment (Phase IV)

## Kubernetes Resources

### Deployment
- **apiVersion**: apps/v1
- **kind**: Deployment
- **metadata**: name, namespace, labels
- **spec**:
  - replicas (integer)
  - selector (matchLabels)
  - template (pod template)
    - metadata (labels)
    - spec (container configuration)
      - containers (array)
        - name, image, ports, resources, envFrom
      - volumes (for configuration)

### Service
- **apiVersion**: v1
- **kind**: Service
- **metadata**: name, namespace, labels
- **spec**:
  - type (NodePort, ClusterIP)
  - selector (to match pods)
  - ports (array)
    - port, targetPort, nodePort (for NodePort services)

### ConfigMap
- **apiVersion**: v1
- **kind**: ConfigMap
- **metadata**: name, namespace
- **data**: key-value pairs for non-sensitive configuration

### Secret
- **apiVersion**: v1
- **kind**: Secret
- **metadata**: name, namespace
- **data**: base64 encoded sensitive data
- **type**: Opaque (for generic key-value pairs)

### Namespace
- **apiVersion**: v1
- **kind**: Namespace
- **metadata**: name

## Helm Chart Structure

### Chart.yaml
- **name**: Chart name (frontend or backend)
- **version**: Semantic version of the chart
- **apiVersion**: Helm API version
- **description**: Brief description of the chart

### values.yaml
- **image**:
  - repository (image name)
  - tag (image version)
  - pullPolicy
- **service**:
  - type (NodePort/ClusterIP)
  - port
- **resources**:
  - requests (cpu, memory)
  - limits (cpu, memory)
- **replicaCount**: Number of pod replicas
- **env**: Environment variables
- **config**: Configuration values

## Docker Configuration

### Dockerfile (Frontend)
- **Base Image**: node:18-alpine
- **Steps**:
  - Copy package files
  - Install dependencies
  - Copy source code
  - Build application
  - Expose port 3000
  - Start application

### Dockerfile (Backend)
- **Base Image**: python:3.11-slim
- **Steps**:
  - Copy requirements
  - Install dependencies
  - Copy source code
  - Expose port 8000
  - Start application

## Environment Configuration

### Frontend Environment Variables
- NEXT_PUBLIC_API_URL (backend API endpoint)
- NEXT_PUBLIC_APP_ENV (application environment)

### Backend Environment Variables
- DATABASE_URL (Neon PostgreSQL connection string)
- JWT_SECRET (authentication secret)
- BETTER_AUTH_SECRET (better-auth secret)
- ENVIRONMENT (development/staging/production)