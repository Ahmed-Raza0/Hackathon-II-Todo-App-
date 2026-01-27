# Use official Node.js runtime as base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies for building)
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js application with placeholder environment variables
RUN NEXT_PUBLIC_BETTER_AUTH_SECRET="placeholder" NEXT_PUBLIC_API_URL="http://backend-service.todo-phase4.svc.cluster.local:8000" npm run build

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"]