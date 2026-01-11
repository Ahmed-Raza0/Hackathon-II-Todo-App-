# Data Model: Production Deployment Configuration Fix

## Frontend Configuration Entities

### EnvironmentConfiguration
- **Fields**:
  - frontendBaseUrl: string (NEXT_PUBLIC_API_BASE_URL)
  - appName: string (NEXT_PUBLIC_APP_NAME)
  - environment: "development" | "production" | "staging"

- **Validation Rules**:
  - frontendBaseUrl must be a valid URL
  - appName must be non-empty string
  - environment must be one of allowed values

### TailwindConfig
- **Fields**:
  - contentPaths: string[] (paths to scan for Tailwind classes)
  - theme: object (custom theme configuration)
  - plugins: string[] (Tailwind plugin paths)

- **Validation Rules**:
  - contentPaths must include App Router directories (/app/**/*)
  - theme must follow Tailwind format
  - plugins must reference valid plugin modules

## Backend Configuration Entities

### ServerConfiguration
- **Fields**:
  - port: number
  - host: string
  - reload: boolean
  - logLevel: string

- **Validation Rules**:
  - port must be between 1024-65535 for non-root users
  - host must be a valid hostname or IP address
  - reload should be false in production
  - logLevel must be valid (debug, info, warning, error)

### CorsConfiguration
- **Fields**:
  - allowedOrigins: string[]
  - allowCredentials: boolean
  - allowedMethods: string[]
  - allowedHeaders: string[]

- **Validation Rules**:
  - allowedOrigins must be valid URLs
  - allowCredentials should be true only for trusted origins
  - allowedMethods must be valid HTTP methods
  - allowedHeaders must include Authorization for JWT

### DatabaseConfiguration
- **Fields**:
  - databaseUrl: string
  - poolSize: number
  - sslRequired: boolean

- **Validation Rules**:
  - databaseUrl must be a valid PostgreSQL connection string
  - poolSize must be positive integer
  - sslRequired should be true in production

### JwtConfiguration
- **Fields**:
  - secret: string
  - algorithm: string
  - expiresIn: string

- **Validation Rules**:
  - secret must be at least 32 characters
  - algorithm must be supported (HS256, HS384, HS512)
  - expiresIn must be valid duration format

## API Contract Entities

### ApiEndpoint
- **Fields**:
  - path: string
  - method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE"
  - requiresAuth: boolean
  - responseFormat: "json"
  - allowedOrigins: string[]

- **Validation Rules**:
  - path must follow REST conventions
  - method must be valid HTTP method
  - requiresAuth must be boolean
  - responseFormat must be JSON
  - allowedOrigins must be valid URLs

## State Transition Models

### DeploymentState
- **States**: local_development → staging → production
- **Transitions**:
  - local_development → staging: Configuration validation passes
  - staging → production: End-to-end testing passes
  - production → maintenance: Hotfix required

### ConfigurationState
- **States**: unconfigured → partially_configured → fully_configured
- **Transitions**:
  - unconfigured → partially_configured: Basic environment variables set
  - partially_configured → fully_configured: All required configurations validated